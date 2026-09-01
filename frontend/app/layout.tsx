import type { Metadata } from "next";
import { DM_Sans } from "next/font/google";
import "./globals.css";
import "./platform.css";

const dmSans = DM_Sans({
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Scotland Open Land",
  description:
    "Open land information for Scotland — Annual Ground Rent at every place.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={dmSans.className}>{children}</body>
    </html>
  );
}
