FROM rasa/rasa:3.1.7-full

WORKDIR /app

ENV HOME=/app

COPY . .

USER 1001

ENTRYPOINT ["rasa"]

CMD ["run","--enable-api","--port","5005","--cors","*"]

