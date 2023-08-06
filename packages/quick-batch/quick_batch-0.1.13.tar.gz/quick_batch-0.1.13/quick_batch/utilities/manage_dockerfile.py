

def check_requirements_copy_and_install(dockerfile_path):
    # Read the Dockerfile
    with open(dockerfile_path, 'r') as file:
        dockerfile_lines = file.readlines()

    # Check if requirements.txt is being copied
    requirements_copied = False
    for line in dockerfile_lines:
        if 'COPY' in line and 'requirements.txt' in line:
            requirements_copied = True
            break

    # Check if requirements.txt is being pip installed
    requirements_installed = False
    for line in dockerfile_lines:
        if 'RUN' in line and 'requirements.txt' in line:
            requirements_installed = True
            break

    if not requirements_copied or not requirements_installed:
        print("INFO: Adding instructions to Dockerfile to copy and "
              "install requirements.txt")
        with open(dockerfile_path, 'a') as file:
            file.write("\nRUN mkdir /usr/src/app\n")
            file.write("COPY requirements.txt /usr/src/app\n")
            file.write("RUN pip install -r /usr/src/app/requirements.txt\n")
            file.write("RUN rm -r /usr/src/app\n")
