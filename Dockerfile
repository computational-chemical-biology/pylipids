FROM continuumio/miniconda:latest
MAINTAINER Ricardo R. da Silva <ridasilva@usp.br>

ENV INSTALL_PATH /home/complex
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY environment.yml environment.yml
RUN conda env create -f environment.yml
RUN echo "source activate complex" > ~/.bashrc
ENV PATH /opt/conda/envs/complex/bin:$PATH


COPY . /home/complex 

ENV FLASK_APP app.py 

EXPOSE 5000
CMD sh /home/zudimentos/run_server.sh 
