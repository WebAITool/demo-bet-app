# --- Стадия 1: Base ---
FROM node:lts-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm install

# --- Стадия 2: Development ---
FROM base AS development
WORKDIR /app
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]

# --- Стадия 3: Builder ---
FROM base AS builder
WORKDIR /app
COPY . .
RUN npm run build

# --- Стадия 4: Production ---
FROM nginx:stable-alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
