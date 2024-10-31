import React from "react";

const Footer = () => {
  return (
    <div>
      <footer className="footer footer-center bg-gray-800 text-base-content p-4">
        <aside>
          <p>
            Copyright © {new Date().getFullYear()} - All right reserved by Jamia Millia Islamia
          </p>
        </aside>
      </footer>
    </div>
  );
};

export default Footer;
