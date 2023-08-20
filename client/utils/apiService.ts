export const search = async (query: string): Promise<{
  start: number;
  end: number;
  text: string;
  link: string;
}[]> => {
  const response = await fetch(`https://dbtp.brunotarijon.com/api/?query=${query}`);
  const data = await response.json();
  return data.results;
};

export const upload = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('https://dbtp.brunotarijon.com/api/', {
    method: 'POST',
    body: formData,
  });
  const data = await response.json();
  return data;
};
