'use client'
import { useRouter } from 'next/navigation'
import { useState, ChangeEvent } from "react";

interface Default {
    defaultValue: string;
}

export const SearchInput = ({ defaultValue }: Default) => {
    const length = 50;
    const router = useRouter()
    const [inputValue, setValue] = useState(defaultValue);

    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        const inputValue = event.target.value;
        setValue(inputValue);
    };

    const handleSearch = () => {
        router.push(`/country?name=${inputValue}`)
    };

    const handleEnter = (event: { key: any }) => {
        if (event.key === "Enter") return handleSearch();
    };

    return (
        <div className="relative w-full">
            <label htmlFor="inputId"></label>
            <input
                type="text"
                id="inputId"
                placeholder="Type a Country Here ..."
                value={inputValue ?? ""}
                onChange={handleChange}
                onKeyDown={handleEnter}
                className="rounded-full w-full py-3 pl-5 pr-14 caret-black p-1 text-black"
                maxLength={length}
            />
            <button
                type="button"
                onClick={handleSearch}
                className="absolute top-0 end-0 h-full w-15 p-2.5 text-sm font-medium text-white bg-slate-900 rounded-e-full hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300">
                <svg
                    className="w-4 h-4"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 20 20"
                >
                    <path
                        stroke="currentColor"
                        strokeLinecap="square"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
                    />
                </svg>
                <span className="sr-only">Search</span>
            </button>
        </div>
    );
}
