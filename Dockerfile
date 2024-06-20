FROM python
WORKDIR /usr/src/app
COPY . .
RUN python3 -m pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
CMD ["python3", "app.py"]