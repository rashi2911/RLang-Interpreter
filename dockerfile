FROM python:latest
WORKDIR /fellowship/
COPY RLang.py /fellowship/
COPY gui.py /fellowship/
CMD python ./gui.py

##COMMANDS TO EXECUTE ON TERMINAL

#1. docker build -t <image_name> <path>
#2. docker run -it <image_name>