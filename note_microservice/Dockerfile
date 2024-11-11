FROM node:20.12.2

# Declaring env
ENV NODE_ENV development

WORKDIR /

# Copying all the files in our project
COPY . .
#installation
RUN npm install

# Starting our application
CMD [ "node", "index.mjs" ]

# Exposing server port
EXPOSE 8080
