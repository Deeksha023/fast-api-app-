import NavBar from "./components/NavBar";
import Welcome from "./components/Welcome";
import Footer from "./components/Footer";
import CompanyCard from "./components/CompanyCard";
import JobCard from "./components/JobCard";
import { useState, useEffect } from "react";
import { getCompanies } from "./Services/CompanyService";
import type { Company } from "./types/company";

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [companies, setCompanies] = useState<Company[]>([]);

  async function fetchCompanies() {
    setLoading(true);

    try {
      const companiesData = await getCompanies();
      setCompanies(companiesData);
      setError(null);
    } catch (err: any) {
      setError(err?.message ?? "Failed to load companies");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchCompanies();
  }, []);

  return (
    <>
      <NavBar />
      <Welcome />
      <br />
      <CompanyCard companies={companies} loading={loading} error={error} />
      <JobCard />
      <Footer />
    </>
  );
}

export default App;