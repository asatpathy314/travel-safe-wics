import { SearchInput } from "../components/SearchBar"

const App = () => {
  return (
    <div className="background__image min-h-screen bg-gradient-to-r from-sky-400 to-blue-500 flex items-center justify-center mx-auto p-4">
        <div className="search__component mx-auto p-4">
            <h1 className="overflow-hidden whitespace-nowrap border-r-4 border-r-white my-5 text-4xl text-white font-bold animate-typing">                    
            {"What's your destination?"}
            </h1>
            <SearchInput defaultValue = ""/>
        </div>
    </div>
)
}

export default App