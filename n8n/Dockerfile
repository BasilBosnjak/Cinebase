FROM node:18-alpine

# Install n8n
RUN npm install -g n8n

# Set working directory
WORKDIR /data

# Set environment variables
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=https
ENV NODE_ENV=production

# Expose port
EXPOSE 5678

# Start n8n
CMD ["npx", "n8n"]
