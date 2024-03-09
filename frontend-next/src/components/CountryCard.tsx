import React, { useState, useEffect } from "react";
import axios from "axios";
import { Failure } from "../components/Failure";

export default function Country(props: any) {
  const name = props.name;
  const [countryJSONObject, setCountryJSONObject] = useState(null);

  // Use useEffect to fetch data when the component mounts
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/?name=${name}`);
        console.log('Successful API Call');
        const data = response.data;
        console.log(data);

        if (data.length > 0) {
          setCountryJSONObject(data[0]);
        } else {
          console.log("WOW THERE");
          // Handle failure case or return a Failure component
        }
      } catch (error) {
        console.error(error);
        // Handle error or return a Failure component
      }
    };

    fetchData();
  }, [name]);

  return (
    <p>Hmmm{JSON.stringify(countryJSONObject)}</p>
  );
}
