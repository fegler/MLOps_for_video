export const videoToChunks = (file, chunkSize) => {
  let offset = 0;
  const chunks = [];
  while (offset < file.size) {
    const end = Math.min(offset + chunkSize, file.size);
    chunks.push(file.slice(offset, end));
    offset += chunkSize;
  }
  return chunks;
};

export const sendVideo = (socket, file, task_name) => {
  const chunkSize = 64 * 1024;
  const chunks = videoToChunks(file, chunkSize);
  chunks.forEach((chunk, index) => {
    const isLastChunk = index === chunks.length - 1;
    socket.emit(task_name, { chunk, isLastChunk });
  });
};
