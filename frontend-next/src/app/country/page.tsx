'use client'
import CountryCard  from "../../components/CountryCard"
import { useSearchParams} from "next/navigation"

const CountryPage = () => {
    const searchParams = useSearchParams();
    const countryName = searchParams.get("name");
    return (
        <main>
            <CountryCard name={countryName}/>
        </main>
    )
}

export default CountryPage