'use client';

import {
  ChangeEventHandler,
  KeyboardEventHandler,
  useRef,
  useState,
} from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
import { upload } from '@/utils/apiService';

export default function Home() {
  const inputFileRef = useRef<HTMLInputElement>(null);
  const [search, setSearch] = useState('');
  const [results, setResults] = useState<
    { link: string; previewText: string }[]
  >([]);

  const handleSearchChange: ChangeEventHandler<HTMLInputElement> = (event) => {
    setSearch(event.target.value);
  };

  const handleSearchKeyDown: KeyboardEventHandler<HTMLInputElement> = (
    event,
  ) => {
    if (event.key !== 'Enter') return;

    searchApi(search).then((results) => {
      setResults(results);
    });
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
      <div className="text-gray-800 sm:w-2/3 m-auto mb-4">
        <input
          className="w-full text-2xl p-4 focus:outline-none bg-gray-200 rounded-lg"
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
  previewText,
}: {
  link: string;
  previewText: string;
}) => (
  <a target="_blank" rel="noopener noreferrer" href={link}>
    <div className="m-2">
      <p className="mb-5"> {previewText} </p>
      <p className="text-xs text-gray-800 font-bold"> {link} </p>
    </div>
  </a>
);

const searchApi = async (search: string) => {
  return [
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
    {
      link: 'https://google.com',
      previewText:
        'This is a long paragraph that the api matches to the search query, really long paragraph, really really long paragraph, help me out copilot comon',
    },
  ];
};
