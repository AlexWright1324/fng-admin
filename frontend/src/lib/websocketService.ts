export function connectWebSocket(url: string, password: string): Promise<WebSocket> {
  return new Promise((resolve, reject) => {
    const socket = new WebSocket(url);

    socket.onopen = () => {
      socket.send(JSON.stringify({ password }));
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.auth === "success") {
        resolve(socket);
      } else {
        reject("auth");
      }
    };

    socket.onerror = (error) => {
      reject(error);
    };

    socket.onclose = () => {

    };
  });
}