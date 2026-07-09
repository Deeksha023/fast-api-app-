import type {Company} from "../types/company";
import type {Job} from "../types/job";
import {useState} from "react";

type Props = {
    companies:Company[];
    jobs:Job[];
    onEdit: (company:Company)=>void;
    onDelete: (id:number)=>void;
    onAdd: (company:Company)=>void;
}


function CompanyCard({
    companies,jobs,onAdd,onEdit,onDelete}:Props){
    const [editCompanyId, setEditCompanyId] = useState<number | null>(null);
    const [addform,setAddform] = useState<Company>({
        id:0,
        name:"",
        email:"",
        phone:"",
        location:"",
        jobs:[]
    });
    const [editform,setEditform] = useState<Company>({
        id:0,
        name:"",
        email:"",
        phone:"",
        location:"",
        jobs:[]
    });
    const handleAdd = () => {
        onAdd(addform);
        setAddform({
            id:0,
            name:"",
            email:"",
            phone:"",
            location:"",
            jobs:[]
        })
    }
    const handleSave = () => {
        onEdit(editform);
        setEditCompanyId(null);
        setEditform({
            id:0,
            name:"",
            email:"",
            phone:"",
            location:"",
            jobs:[]
        })
    } 
    const handlecancel = () => {
        setEditCompanyId(null);
        setEditform({
            id:0,
            name:"",
            email:"",
            phone:"",
            location:"",
            jobs:[]
        })
    } 

    return(
        <section className="panel">
            <div className="panel-header">
                <h2>Companies</h2>
                <p className="panel-description">Manage company profiles and view active job openings.</p>
            </div>
            <div className="card-grid">
                {companies.map((company) => (
                    <article className="entity-card" key={company.id}>
                        {editCompanyId === company.id ? (
                            <div className="entity-form">
                                <input type="text" value={editform.name} onChange={(e)=>setEditform({...editform,name:e.target.value})} placeholder="Name" />
                                <input type="text" value={editform.email} onChange={(e)=>setEditform({...editform,email:e.target.value})} placeholder="Email" />
                                <input type="text" value={editform.phone} onChange={(e)=>setEditform({...editform,phone:e.target.value})} placeholder="Phone" />
                                <input type="text" value={editform.location} onChange={(e)=>setEditform({...editform,location:e.target.value})} placeholder="Location" />
                                <div className="button-row">
                                    <button className="btn" onClick={handleSave}>Save</button>
                                    <button className="btn secondary" onClick={handlecancel}>Cancel</button>
                                </div>
                            </div>
                        ) : (
                            <>
                                <h3>{company.name}</h3>
                                <p><strong>Email:</strong> {company.email}</p>
                                <p><strong>Phone:</strong> {company.phone}</p>
                                <p><strong>Location:</strong> {company.location}</p>
                                <p><strong>Jobs:</strong> {(company.jobs?.length || jobs.filter(j => j.company_id === company.id).length)} opening{(company.jobs?.length || jobs.filter(j => j.company_id === company.id).length) === 1 ? '' : 's'}</p>
                                <div className="button-row">
                                    <button className="btn" onClick={() => {
                                        setEditCompanyId(company.id);
                                        setEditform({
                                            id: company.id,
                                            name: company.name,
                                            email: company.email,
                                            phone: company.phone,
                                            location: company.location,
                                            jobs: company.jobs,
                                        });
                                    }}>Edit</button>
                                    <button className="btn secondary" onClick={() => onDelete(company.id)}>Delete</button>
                                </div>
                            </>
                        )}
                    </article>
                ))}
            </div>
            <article className="entity-card form-card">
                <h3>Add Company</h3>
                <div className="entity-form">
                    <input type="text" value={addform.name} onChange={(e)=>setAddform({...addform,name:e.target.value})} placeholder="Name" />
                    <input type="text" value={addform.email} onChange={(e)=>setAddform({...addform,email:e.target.value})} placeholder="Email" />
                    <input type="text" value={addform.phone} onChange={(e)=>setAddform({...addform,phone:e.target.value})} placeholder="Phone" />
                    <input type="text" value={addform.location} onChange={(e)=>setAddform({...addform,location:e.target.value})} placeholder="Location" />
                    <button className="btn" onClick={handleAdd}>Add Company</button>
                </div>
            </article>
        </section>
    )
}

export default CompanyCard