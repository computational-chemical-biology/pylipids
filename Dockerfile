FROM continuumio/miniconda:latest
MAINTAINER Ricardo R. da Silva <ridasilva@usp.br>

ENV INSTALL_PATH /home/pylipids
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY environment.yml environment.yml
RUN conda env create -f environment.yml
RUN echo "source activate pylipids" > ~/.bashrc
ENV PATH /opt/conda/envs/pylipids/bin:$PATH


COPY . /home/pylipids 
RUN conda install -c anaconda graphviz

ENV FLASK_APP app.py 

EXPOSE 5000
CMD sh /home/pylipids/run_server.sh 
