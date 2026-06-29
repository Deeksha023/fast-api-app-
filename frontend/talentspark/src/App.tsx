import NavBar from "./components/NavBar";
import Welcome from "./components/Welcome";
import Footer from "./components/Footer";
import CompanyCard from "./components/CompanyCard";
import JobCard from "./components/JobCard";

function App() {
  return (
    <>
      <NavBar />
      <Welcome />
      <CompanyCard />
      <JobCard />
      <Footer />
    </>
  );
}

export default App;