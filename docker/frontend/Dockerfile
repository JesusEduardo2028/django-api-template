FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY ./frontend/package*.json ./

# Install all dependencies
RUN npm install

# Copy frontend code
COPY ./frontend /app

# Expose port for React dev server
EXPOSE 3000

# Start development server
CMD ["npm", "start"]
