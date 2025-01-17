import Link from 'next/link';
import './globals.css';

export const metadata = {
  title: 'Kineton',
  description: 'Welcome to Kineton!',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <nav>
          <Link href="/">
            <h1>Kineton</h1>
          </Link>
          <Link href="/contact">
            Contact Us
          </Link>
        </nav>
        {children}
      </body>
    </html>
  );
}
