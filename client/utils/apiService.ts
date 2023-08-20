export const search = async (query: string) => {
  const response = await fetch(`http://localhost:8000/?q=${query}`);
  const data = await response.json();
  return data;
};

export const upload = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('http://localhost:8000/', {
    method: 'POST',
    body: formData,
  });
  const data = await response.json();
  return data;
};
