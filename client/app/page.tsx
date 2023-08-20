'use client';

import {
  ChangeEventHandler,
  KeyboardEventHandler,
  useRef,
  useState,
} from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
import { upload, search } from '@/utils/apiService';

export default function Home() {
  const inputFileRef = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<
    { link: string; text: string, start: number, end: number, }[]
  >([]);

  const handleSearchChange: ChangeEventHandler<HTMLInputElement> = (event) => {
    setQuery(event.target.value);
  };

  const handleSearchKeyDown: KeyboardEventHandler<HTMLInputElement> = async (
    event,
  ) => {
    if (event.key !== 'Enter') return;

    const res = await search(query);
    console.log(res);
    if (!res) return;
    setResults(res);
  };

  const handleFileUploadClick = () => {
    inputFileRef.current?.click();
  };

  const handleFileUploadChange: ChangeEventHandler<HTMLInputElement> = async (
    event,
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      await upload(file);
    } catch (error) {
      alert(error);
      return;
    }
    alert('File uploaded successfully');
  };

  return (
    <main className="font-mono flex flex-col h-screen antialiased">
      <div className="sm:w-2/3 m-auto mb-4 mt-20">
        <h1 className="text-4xl font-bold text-gray-200">Search</h1>
        <input
          className="w-full text-gray-800 text-2xl p-4 mt-5 focus:outline-none bg-gray-200 rounded-lg"
          type="text"
          onChange={handleSearchChange}
          onKeyDown={handleSearchKeyDown}
        />
      </div>
      <div className="m-auto bg-gray-200 rounded-lg flex flex-col sm:w-2/3 text-gray-800">
        {results.map((result, index) => (
          <div
            key={index}
            className="cursor-pointer hover:bg-gray-300 rounded-xl"
          >
            <PreviewLinkCard {...result} />
            <div className="border-gray-800 border-b" />
          </div>
        ))}
      </div>
      <div className="flex flex-col sm:w-2/3 m-auto mt-4">
        <button
          className="text-2xl w-1/4 rounded-lg p-4 m-auto bg-gray-300 hover:bg-gray-400"
          onClick={handleFileUploadClick}
        >
          <FontAwesomeIcon icon={faUpload} />
        </button>
        <input
          className="hidden"
          ref={inputFileRef}
          type="file"
          name="file"
          onChange={handleFileUploadChange}
        />
      </div>
    </main>
  );
}

const PreviewLinkCard = ({
  link,
  text,
  start,
}: {
  link: string;
  text: string;
  start: number;
}) => {
  const linkFileName = link.split('/').pop() || '';

  const videoLinksPerLinkFile = {
    [linkFileName]: `invalidUrl(${linkFileName})`,
    'matematica-enem.mp4': `https://youtu.be/MSZdhDBoXe0?t=${Math.trunc(start)}`,
    '5 TA\u0303\u0093PICOS MAIS IMPORTANTES DE GEOGRAFIA PARA O ENEM | Prof. Leandro Almeida.mp4': `https://youtu.be/Z_Pb2hWneog?t=${Math.trunc(start)}`,
  }

  return (
  <a target="_blank" rel="noopener noreferrer" href={videoLinksPerLinkFile[linkFileName]}>
    <div className="m-2">
      <p className="mb-5"> {`..."${text}"...`} </p>
      <p className="text-xs text-gray-800 font-bold"> {videoLinksPerLinkFile[linkFileName]} </p>
    </div>
  </a>
)};
