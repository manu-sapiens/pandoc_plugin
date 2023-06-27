# --------------- SHARED -------------------------------------------
print(f"RUNNING: {__name__} ")
import sys
sys.path.append('.')  # Add the current directory to the sys path
sys.path.append('utils')  # Add the current directory to the sys path
from utils.omni_utils_misc import omni_get_env
from utils.omni_utils_http import CdnHandler, route_commands
routes_info = {}
cdn = CdnHandler()
# ------------------------------------------------------------------
OMNI_TEMP_FOLDER = omni_get_env("OMNI_TEMP_FOLDER")
OMNI_PLUGINS_DIR = omni_get_env("OMNI_PLUGINS_FOLDER")



import subprocess
import os

# --------------- PANDOC CONVERT ---------------------
from Plugins.pandoc_plugin.pandoc_plugin import PandocConvert_Input,  PandocConvert_Response, ENDPOINT_PANDOC_CONVERT
async def PandocConvert_HandlePost(input: PandocConvert_Input):
    plugin_name = "pandoc_plugin"
    if True:
        print("------------- convert ------------------")
        print(f"input = {input}")
        input_cdns = input.documents
        input_format = input.input_format
        output_format = input.output_format
        input_filenames = await cdn.download_files_from_cdn(input_cdns)
        print(f"input_filenames = {input_filenames}")

        result_filenames = []
        results_cdns = []

        pandoc_command = f"cd {OMNI_PLUGINS_DIR} && cd {plugin_name} && pandoc"
        for input_filename in input_filenames:
            # Split the file name and extension
            base_filename, file_extension = os.path.splitext(input_filename)

            # If 'auto' is selected, the format is guessed by pandoc (represented by an empty string)
            input_format = '' if input_format.lower() == 'auto' else input_format.lower()
            output_format = output_format.lower()

            # Create output file name
            output_filename = f"{base_filename}_converted.{output_format}"
            
            # Construct pandoc command
            command = pandoc_command

            # Append formats to command
            if input_format:
                command += f' --from {input_format}'
            #
            command += f' --to {output_format}'

            command += f' --standalone'
            """Produce output with an appropriate header and footer (e.g. a standalone HTML, LaTeX, TEI, or RTF file, 
            not a fragment). This option is set automatically for pdf, epub, epub3, fb2, docx, and odt output. 
            For native output, this option causes metadata to be included; otherwise, metadata is suppressed."""

            command += f' -o {os.path.abspath(output_filename)}'  # output file name
            command += f" {os.path.abspath(input_filename)}"  # input file name

            print(f"[pandoc] command = {command}")
            # Execute command
            try:
                print("Running pandoc...")
                subprocess.Popen(command, shell=True, start_new_session=True).wait()
                print("Running done...")
                
                result_filenames.append(output_filename)

                print(f"File converted successfully! Output file: {output_filename}")

            except subprocess.CalledProcessError as e:
                print(f"Pandoc failed: {e}")
            #
        #

        print(f"result_filenames = {result_filenames}")
        if result_filenames != None:  
            results_cdns = await cdn.upload_files_to_cdn(result_filenames)

        # delete the results files from the local storage
        cdn.delete_temp_files(result_filenames)

        return PandocConvert_Response(media_array=results_cdns) 
routes_info[ENDPOINT_PANDOC_CONVERT] = (PandocConvert_Input, PandocConvert_HandlePost)

# --------------- SHARED -------------------------------------------
if __name__ == '__main__':
    route_commands(routes_info, sys.argv)
# ------------------------------------------------------------------