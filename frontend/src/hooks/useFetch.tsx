import { useState, useEffect } from "react";
import axios from "axios";
import { baseUrl } from "../shared";

export default function useGet(url: string, token: string) {
  const [data, setData] = useState<object>();
  const fullUrl: string = baseUrl + url;

  useEffect(() => {
    axios
      .get(fullUrl, { headers: { Authorization: `Bearer ${token}` } })
      .then((response) => setData(response.data));
  }, []);
  return data;
}
