import typer
import subprocess
import sys
from .utilities.connections import access_to

app = typer.Typer()

@app.command()
def install(model: str):

    models = ["grc_perseus_sm","grc_perseus_lg","grc_perseus_trf","grc_proiel_sm","grc_proiel_lg","grc_proiel_trf"]

    hf_url = "https://huggingface.co/"

    if model in models:

        # Checking the access to Hugging Face
        if not access_to(hf_url):
            print(f'The access to {hf_url} is not possible.')
            print(f'Please, check the network connection.')
            exit(0)

        # The url for the model
        https = hf_url + "Jacobo/" + model + "/resolve/main/" + model + "-any-py3-none-any.whl"

        # The pip command
        pip_command = "python -m pip install " + https

        try:
            process = subprocess.Popen(pip_command.split(" "),
                                       bufsize=1,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)
        except Exception as e:

            print(f'There is a problem with  the command: {pip_command}')
            print(f'Below the related information:')
            print(f'{str(e)}')

        else:

            finished = process.poll()

            if not finished:

                print('\n' + f'Installing {model}.....')
                print('\n' + f'Please wait, this could take some minutes.....' + '\n')

                while True:

                    msg = process.stdout.readline()
                    print(msg.strip())
                    return_code = process.poll()
                    if return_code is not None:
                        # The model was successfully installed
                        # Printing the rest of the installation's output:
                        for msg in process.stdout.readlines():
                            print(msg.strip())
                        break

            else:
                print(f'The model: {model} can not be installed' + '\n')
                print("Please, check the model's name in the address below." + '\n')
                print(https + '\n')
                print('Error CODE', error, '\n')
                # The model can not be installed
                # Printing the rest of the error's output:
                for msg in process.stderr.readline():
                    print(msg)
    else:
        print('\n' + f'Please, check the model required. The options in greCy are:')
        print([model for model in models])


@app.command()
def uninstall(model: str):

    models = ["grc_perseus_sm","grc_perseus_lg","grc_perseus_trf","grc_proiel_sm","grc_proiel_lg","grc_proiel_trf"]

    if model in models:

        pip_command = "python -m pip uninstall --yes " + model

        try:
            process = subprocess.Popen(pip_command.split(" "),
                                       bufsize=1,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)
        except Exception as e:

            print(f'There is a problem with the command: {pip_command}')
            print(f'Below the related information:')
            print(f'{str(e)}')

        else:

            error = process.stderr.readline()

            if error:
                print(error)
                exit(0)

            else:

                while True:

                    msg = process.stdout.readline()
                    print(msg)
                    return_code = process.poll()

                    if return_code is not None:
                        # The model has been uninstalled.
                        # Printing the rest of the output:
                        for msg in process.stdout.readlines():
                            print(msg)
                        break
    else:
        print(f'The model: {model} can not be uninstalled' + "\n")
        print(f'Please, check the model. The options in greCy are:')
        print([model for model in models])

if __name__ == "__main__":

    app()
