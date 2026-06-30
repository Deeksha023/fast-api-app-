import type { Company } from "../types/company";

interface CompanyCardProps {
  companies: Company[];
  loading: boolean;
  error: string | null;
}

function CompanyCard({ companies, loading, error }: CompanyCardProps) {
  if (loading) {
    return <div>Loading companies...</div>;
  }

  if (error) {
    return <div>Error loading companies: {error}</div>;
  }

  return (
    <div>
      <h2>Companies</h2>
      {companies.length === 0 ? (
        <p>No companies found.</p>
      ) : (
        companies.map((company) => (
          <div key={company.id}>
            <h1>{company.name}</h1>
            <p>Email: {company.email}</p>
            <p>Phone: {company.phone}</p>
            <p>Location: {company.location}</p>
            <hr />
          </div>
        ))
      )}
    </div>
  );
}

export default CompanyCard;