import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

interface CardProps {
  f_name: string;
  l_name: string;
  wallet_name: string;
  currency: string;
}

export default function WalletCard(props: CardProps) {
  const f_name = props.f_name;
  const l_name = props.l_name;
  const wallet_name = props.wallet_name;
  const currency = props.currency;
  return (
    <Card sx={{ minWidth: 500 }}>
      <CardContent>
        <Typography variant="h4" component="div">
          {wallet_name} Wallet
        </Typography>
        <Typography variant="h5" component="div">
          {f_name} {l_name}
        </Typography>
        <Typography variant="body2">
          0.00 {currency}
          <br />
          {"Your default wallet, not shared with anybody yet"}
        </Typography>
      </CardContent>
    </Card>
  );
}
