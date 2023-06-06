export default function formatNumber(number: string) {
    const formattedString = number.replace(
      /^(\d{4})(\d{4})(\d{4})(\d{4})$/,
      "$1 XXXX XXXX $4"
    );
    return formattedString;
  }
