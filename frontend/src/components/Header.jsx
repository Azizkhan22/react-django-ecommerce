import { MdCall, MdMail } from 'react-icons/md';
import { FaInstagram, FaFacebook, FaYoutube, FaTwitter } from 'react-icons/fa';

function Header() {
  return (
    <header className="bg-gray-800 text-white p-4">
        <div className='grid grid-cols-3 items-center'>
            <div className="flex justify-between items-center pl-2">
                <div>
                    <MdCall className="inline-block mr-1" />
                    <span className="text-sm">+1 234 567 890</span>
                </div>
                <div>
                    <MdMail className="inline-block mr-1" />
                    <span className="text-sm" >khan@gmail.com</span>  
                </div>
            </div>
            <div>
                <p className='text-sm flex justify-end items-center'>Follow Us  and get a chance to win 80% off</p>
            </div>
            <div className='flex justify-end items-center space-x-2 pr-2'>
                <span className='text-sm font-bold'>Follow Us</span>
                <span>:</span>
                <FaInstagram className="inline-block mx-1 text-base cursor-pointer" />
                <FaYoutube className="inline-block mx-1 text-base cursor-pointer" />                 
                <FaFacebook className="inline-block mx-1 text-base cursor-pointer" />               
                <FaTwitter className="inline-block mx-1 text-base cursor-pointer" /> 
            </div>
        </div>
        <nav>
          <ul className="flex space-x-4">
            <li><a href="/" className="hover:underline">Home</a></li>
            <li><a href="/products" className="hover:underline">Products</a></li>
            <li><a href="/cart" className="hover:underline">Cart</a></li>
          </ul>
        </nav>      
    </header>
  );
}

export default Header;