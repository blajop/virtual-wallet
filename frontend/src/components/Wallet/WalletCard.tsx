import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

interface CardProps {
  name: string;
  walletName: string;
  currency: string;
  balance: string;
}

export default function WalletCard(props: CardProps) {
  const name = props.name;
  const walletName = props.walletName;
  const currency = props.currency;
  const balance = props.balance;
  return (
    <Card sx={{ minWidth: 500 }}>
      <CardContent>
        <Typography variant="h4" component="div">
          {walletName} Wallet
        </Typography>
        <Typography variant="h5" component="div">
          {name}
        </Typography>
        <Typography variant="body2">
          {balance} {currency}
          <br />
          {"Your default wallet, not shared with anybody yet"}
        </Typography>
      </CardContent>
    </Card>
  );
}
