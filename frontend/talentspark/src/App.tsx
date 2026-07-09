import NavBar from "./components/NavBar";
import CompanyCard from "./components/CompanyCard";
import JobCard from "./components/JobCard";
import Footer from "./components/Footer";
import { useEffect, useState } from "react";
import { getCompanies, updateCompany, deleteCompany, createCompany } from "./Services/CompanyService";
import { getJobs, updateJob, deleteJob, createJob } from "./Services/JobService";
import type { Company } from "./types/company"
import type { Job } from "./types/job"
import Login from "./pages/login";
import Register from "./pages/Register";
import Chat from "./pages/chat";
import ResumeAnalysis from "./pages/ResumeAnalysis";
import { getAxiosErrorMessage } from "./Services/api";
import "./App.css";

function getErrorMessage(error: unknown) {
  return getAxiosErrorMessage(error);
}

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null)
  const [companies, setCompanies] = useState<Company[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [page, setPage] = useState<"login" | "register">("login");
  const [currentPage, setCurrentPage] = useState<"home" | "chat" | "resume">(() => {
    if (typeof window !== "undefined") {
      if (window.location.pathname === "/resume") return "resume";
      if (window.location.pathname === "/chat") return "chat";
    }
    return "home";
  });

  const handleLogin = (newToken: string) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  async function fetchData() {
    setLoading(true);
    try {
      const [companiesData, jobsData] = await Promise.all([
        getCompanies(),
        getJobs()
      ]);
      setCompanies(companiesData);
      setJobs(jobsData);
    } catch (error) {
      setError(new Error(getErrorMessage(error)));
    } finally {
      setLoading(false);
    }
  }

  async function handleEdit(company: Company) {
    try {
      const updatedCompany = await updateCompany(company.id, company);
      setCompanies(prev =>
        prev.map(company =>
          company.id === updatedCompany.id ? updatedCompany : company
        )
      );
    } catch (error) {
      setError(new Error(getErrorMessage(error)));
    }
  }

  async function handleDelete(id: number) {
    try {
      await deleteCompany(id);
      setCompanies(prev =>
        prev.filter(company => company.id !== id)
      );
    } catch (error) {
      setError(new Error(getErrorMessage(error)));
    }
  }

  async function handleAdd(company: Company) {
    try {
      const newCompany = await createCompany(company);
      setCompanies(prev => [...prev, newCompany]);
    } catch (error) {
      setError(new Error(getErrorMessage(error)));
    }
  }

  async function handleJobEdit(job: Job) {
    try {
      const updatedJob = await updateJob(job.id, job);
      setJobs(prev =>
        prev.map(j =>
          j.id === updatedJob.id ? updatedJob : j
        )
      );
    } catch (error) {
      setError(new Error(getErrorMessage(error)));
    }
  }

  async function handleJobDelete(id: number) {
    try {
      await deleteJob(id);
      setJobs(prev =>
        prev.filter(job => job.id !== id)
      );
    } catch (error) {
      setError(new Error(getErrorMessage(error)));
    }
  }

  async function handleJobAdd(job: Job) {
    try {
      const newJob = await createJob(job);
      setJobs(prev => [...prev, newJob]);
    } catch (error) {
      setError(new Error(getErrorMessage(error)));
    }
  }


  useEffect(() => {
    if (token) {
      fetchData();
    }
  }, [token]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const path = window.location.pathname;
    if (path === "/resume") setCurrentPage("resume");
    else if (path === "/chat") setCurrentPage("chat");
    else setCurrentPage("home");

    const handlePopState = () => {
      const path = window.location.pathname;
      if (path === "/resume") setCurrentPage("resume");
      else if (path === "/chat") setCurrentPage("chat");
      else setCurrentPage("home");
    };

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const targetPath = currentPage === "resume" ? "/resume" : currentPage === "chat" ? "/chat" : "/";
    if (window.location.pathname !== targetPath) {
      window.history.pushState(null, "", targetPath);
    }
  }, [currentPage]);

  if (!token) {
    return (
      <>
        {page === "login" ? (
          <Login onLogin={handleLogin} onSwitchToRegister={() => setPage("register")} />
        ) : (
          <Register onSwitchToLogin={() => setPage("login")} />
        )}
      </>
    )
  }

  if (loading) {
    return <div>Loading...</div>
  }

  if (error) {
    return <div className="status-message">Error: {error.message}</div>
  }
  return (
    <div className="app-shell">
      <NavBar currentPage={currentPage} onNavigate={setCurrentPage} />
      <main className="main-content">
        {currentPage === "home" && (
          <>
            <CompanyCard
              companies={companies}
              jobs={jobs}
              onEdit={handleEdit}
              onDelete={handleDelete}
              onAdd={handleAdd}
            />
            <JobCard
              jobs={jobs}
              companies={companies}
              onEdit={handleJobEdit}
              onDelete={handleJobDelete}
              onAdd={handleJobAdd}
            />
          </>
        )}
        {currentPage === "resume" && <ResumeAnalysis />}
        {currentPage === "chat" && <Chat />}
      </main>
      <Footer />
    </div>
  )
}

export default App




