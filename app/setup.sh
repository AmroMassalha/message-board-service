#!/bin/bash

echo "====================================="
echo "Message Board Setup Script"
echo "====================================="
echo ""
echo "This script will guide you through the setup of the Message Board application."
echo "Please pay attention to the prompts for messages."
echo "This script may ask for your sudo permission in order to install necessary dependencies."
echo ""
echo "Please ensure you have a stable internet connection before proceeding."
echo "Press any key to continue or Ctrl+C to exit..."
read -n1

PYTHON_MINIMUM_VERSION="3.10"
PYTHON_INSTALLED=$(python3 --version 2>&1 | awk '{print $2}')

if [[ "$(printf '%s\n' "$PYTHON_MINIMUM_VERSION" "$PYTHON_INSTALLED" | sort -V | head -n1)" != "$PYTHON_MINIMUM_VERSION" ]]; then
    echo "====================================="
    echo "Python 3.10 or higher is required."
    echo "====================================="
    echo ""
    read -r -p "Would you like to install Python 3.10? [Y/n] " response
    case "$response" in
        [yY][eE][sS]|[yY])
            echo "Detecting Operating System."
            if [ "$(uname)" == "Darwin" ]; then
                # MacOS
                echo "MacOS detected."
                command -v brew >/dev/null 2>&1 || {
                    echo >&2 "Homebrew is required but it's not installed. Install Homebrew now? [Y/n]"; read -r answer;
                    if echo "$answer" | grep -iq "^y" ;then
                        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                    else
                        echo "Python is required. Exiting."; exit 1;
                    fi
                }
                echo "=================="
                echo "Installing Python."
                echo "=================="
                echo ""
                brew install python@3.10
            else
                # Linux
                echo "==============="
                echo "Linux detected."
                echo "==============="
                echo ""
                if [ -f /etc/os-release ]; then
                    . /etc/os-release
                    case $ID in
                        debian|ubuntu|devuan)
                            sudo apt-get update
                            # Check Python
                            if ! command -v python3.10 &> /dev/null; then
                                echo "Python 3.10 is not installed. Would you like to install it? (y/n)"
                                read answer
                                if [ "$answer" == "y" ]; then
                                    sudo apt-get install python3.10 -y
                                else
                                    echo "Python 3.10 is required. Exiting."; exit 1;
                                fi
                            fi
                            # Check Docker
                            if ! command -v docker &> /dev/null; then
                                echo "==========================================================="
                                echo "Docker is not installed. Would you like to install it? (y/n)"
                                echo "==========================================================="
                                echo ""
                                read answer
                                if [ "$answer" == "y" ]; then
                                    sudo apt-get install docker.io -y
                                    sudo systemctl start docker
                                    sudo systemctl enable docker
                                else
                                    echo "Docker is required. Exiting."; exit 1;
                                fi
                            fi
                            # Check Docker Compose
                            if ! command -v docker-compose &> /dev/null; then
                                echo "==================================================================="
                                echo "Docker Compose is not installed. Would you like to install it? (y/n)"
                                echo "==================================================================="
                                echo ""
                                read answer
                                if [ "$answer" == "y" ]; then
                                    sudo apt-get install docker-compose -y
                                else
                                    echo "Docker Compose is required. Exiting."; exit 1;
                                fi
                            fi
                            ;;
                        centos|fedora|rhel)
                            sudo yum update
                            # Check Python
                            if ! command -v python3.10 &> /dev/null; then
                                echo "================================================================"
                                echo "Python 3.10 is not installed. Would you like to install it? (y/n)"
                                echo "================================================================"
                                echo ""
                                read answer
                                if [ "$answer" == "y" ]; then
                                    sudo yum install python3.10 -y
                                else
                                    echo "Python 3.10 is required. Exiting."; exit 1;
                                fi
                            fi
                            # Check Docker
                            if ! command -v docker &> /dev/null; then
                                echo "==========================================================="
                                echo "Docker is not installed. Would you like to install it? (y/n)"
                                echo "==========================================================="
                                echo ""
                                read answer
                                if [ "$answer" == "y" ]; then
                                    sudo yum install docker -y
                                    sudo systemctl start docker
                                    sudo systemctl enable docker
                                else
                                    echo "Docker is required. Exiting."; exit 1;
                                fi
                            fi
                            # Check Docker Compose
                            if ! command -v docker-compose &> /dev/null; then
                                echo "==================================================================="
                                echo "Docker Compose is not installed. Would you like to install it? (y/n)"
                                echo "==================================================================="
                                echo ""
                                read answer
                                if [ "$answer" == "y" ]; then
                                    sudo yum install docker-compose -y
                                else
                                    echo "Docker Compose is required. Exiting."; exit 1;
                                fi
                            fi
                            ;;
                        *)
                            echo "Unsupported Linux distribution. Exiting."; exit 1;
                            ;;
                    esac
                else
                    echo "Could not determine Linux distribution. Exiting."; exit 1;
                fi
            fi
            ;;
        *)
            echo "Python is required. Exiting."; exit 1;
            ;;
    esac
fi

# Create virtual environment
echo "============================="
echo "Creating virtual environment."
echo "============================="
echo ""
python3.10 -m venv ./venv

# Activate virtual environment
echo "=============================="
echo "Activating virtual environment."
echo "=============================="
echo ""
source ./venv/bin/activate

# Install requirements
echo "========================"
echo "Installing requirements."
echo "========================"
echo ""
pip install -r ./requirements.txt

# Change the directory up, Install pre-commit and then change back
pushd ..
echo "============================"
echo "Installing pre-commit hooks."
echo "============================"
echo ""
source ./app/venv/bin/activate
pre-commit install
popd

# Build and run docker compose
echo "======================="
echo "Running Docker compose."
echo "======================="
echo ""
docker-compose up -d --build

echo "Message Board App is now running!"
