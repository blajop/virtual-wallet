import axios from "axios";
import { apiUrl } from "../shared";
import { Friend } from '../components/ProfilePageComponents/FriendBox';

type User = Friend;

export default async function retrieveUser(userId: string): Promise<User> {
    const response = await axios.get(apiUrl + `users/${userId}`, {
      headers: { Authorization: `Bearer ${localStorage.token}` },
    });
    
    return response.data;
  
}
