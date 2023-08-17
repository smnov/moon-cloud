import Image from 'next/image'
import  Header from './components/Header/Header.tsx'
import UserFiles from './components/UserFiles/UserFiles.tsx'

export default function Home() {
  return (
    <div>
    <Header />
    <UserFiles />
      </div>
  )
}
