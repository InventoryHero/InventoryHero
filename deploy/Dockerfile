FROM node:lts-alpine
RUN npm install -g http-server

WORKDIR /app

COPY package*.json ./


RUN npm install

COPY . .

RUN npm run build
ENV VUE_APP_URL="https://etzqzuvagicmnzfkjcuc.supabase.co"
ENV VUE_APP_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV0enF6dXZhZ2ljbW56ZmtqY3VjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4MjY4MjQ2MCwiZXhwIjoxOTk4MjU4NDYwfQ.8dW69oGS1Ue34ZKtldQcXaSZ2mjfmpRgU_dHTZfxJYg"


EXPOSE 8080
CMD ["http-server", "dist"]