FROM continuumio/miniconda3:latest

WORKDIR /app

COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml && conda clean -afy

ENV CONDA_DEFAULT_ENV=webserver
ENV PATH=/opt/conda/envs/webserver/bin:$PATH

COPY app.py settings.py .env app_AB_test.py /app/
COPY util/ /app/util/
COPY service_adapters/ /app/service_adapters/

EXPOSE 8501
CMD ["streamlit", "run", "app_AB_test.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
