FROM python:3.12-slim

RUN pip install mangum uvicorn httpx fastapi
RUN pip install osbot-aws osbot-fast-api
RUN pip install cbr-shared

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

RUN python --version
ENV PORT=8080

WORKDIR /app
COPY ../../../cbr_user_session /app/cbr_user_session

ENV PYTHONPATH="/app"

COPY ./deploy/docker/cbr-user-session/start.sh /app/start.sh

CMD ["./start.sh"]

