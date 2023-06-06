import * as React from "react";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import CreditCardIcon from "@mui/icons-material/CreditCard";
import { Card } from "../../pages/Profile";
import { apiUrl } from "../../shared";
import axios from "axios";
import formatNumber from "../../functions/formatNumber";

export default function SelectCard({
  username,
  token,
  setCard,
}: {
  username: string;
  token: string;
  setCard: (card: Card | undefined) => void;
}) {
  const [selectedCardId, setSelectedCardId] = React.useState<string>("");
  const [allCards, setAllCards] = React.useState<Card[]>([]);

  const handleChange = (event: SelectChangeEvent<string>) => {
    setSelectedCardId(event.target.value);
    const selectedCard = allCards.find(
      (card) => card.id === event.target.value
    );
    setCard(selectedCard);
  };

  React.useEffect(() => {
    if (username)
      axios
        .get(apiUrl + `cards/user/${username}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => {
          setAllCards(response.data);
          if (response.data.length > 0) {
            setCard(response.data[0]);
            setSelectedCardId(response.data[0].id); // Set the ID of the first card as the default
          }
        });
  }, [username]);

  return (
    <FormControl
      sx={{
        mt: 1,
        width: "100%",
        backgroundColor: "white",
        color: "black",
        display: "flex",
        paddingY: "0px",
      }}
      size="small"
    >
      <Select
        displayEmpty={false}
        labelId="demo-select-small-label"
        id="demo-select-small"
        value={selectedCardId}
        onChange={handleChange}
        sx={{
          color: "black",
        }}
      >
        {allCards.map((card, index) => (
          <MenuItem
            key={index}
            value={card.id}
            sx={{
              display: "flex",
              alignItems: "center",
            }}
          >
            <CreditCardIcon /> {"  "}
            {formatNumber(card.number)}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
