import type {Job} from "../types/job";
import type {Company} from "../types/company";

import {useState} from "react";

type Props = {
    jobs:Job[];
    companies:Company[];
    onEdit: (job:Job)=>void;
    onDelete: (id:number)=>void;
    onAdd: (job:Job)=>void;
}

function JobCard({
    jobs,companies,onEdit,onDelete,onAdd}:Props){
        const [editJobId, setEditJobId] = useState<number | null>(null);
        const [addform,setAddform] = useState<Job>({
            id:0,
            title:"",
            description:"",
            salary:"",
            company_id:0
        });
        const [editform,setEditform] = useState<Job>({
            id:0,
            title:"",
            description:"",
            salary:"",
            company_id:0
        });
        const handleAdd = () => {
            onAdd(addform);
            setAddform({
                id:0,
                title:"",
                description:"",
                salary:"",
                company_id:0
            })
        }
        const handleSave = () => {
            onEdit(editform);
            setEditJobId(null);
            setEditform({
                id:0,
                title:"",
                description:"",
                salary:"",
                company_id:0
            })
        }
        const handlecancel = () => {
            setEditJobId(null);
            setEditform({
                id:0,
                title:"",
                description:"",
                salary:"",
                company_id:0
            })
        }

    return(
        <section className="panel">
            <div className="panel-header">
                <h2>Jobs</h2>
                <p className="panel-description">Track open roles and assign them to the right company.</p>
            </div>
            <div className="card-grid">
                {jobs.map((job) => (
                    <article className="entity-card" key={job.id}>
                        {editJobId === job.id ? (
                            <div className="entity-form">
                                <input type="text" value={editform.title} onChange={(e)=>setEditform({...editform,title:e.target.value})} placeholder="Title" />
                                <input type="text" value={editform.description} onChange={(e)=>setEditform({...editform,description:e.target.value})} placeholder="Description" />
                                <input type="text" value={editform.salary} onChange={(e)=>setEditform({...editform,salary:e.target.value})} placeholder="Salary" />
                                <input type="number" value={editform.company_id} onChange={(e)=>setEditform({...editform,company_id:Number(e.target.value)})} placeholder="Company ID" />
                                <div className="button-row">
                                    <button className="btn" onClick={handleSave}>Save</button>
                                    <button className="btn secondary" onClick={handlecancel}>Cancel</button>
                                </div>
                            </div>
                        ) : (
                            <>
                                <h3>{job.title}</h3>
                                <p>{job.description}</p>
                                <div className="inline-meta">
                                    <span>Salary: {job.salary}</span>
                                    <span>Company: {companies.find(c => c.id === job.company_id)?.name || job.company_id}</span>
                                </div>
                                <div className="button-row">
                                    <button className="btn" onClick={() => {
                                        setEditJobId(job.id);
                                        setEditform({
                                            id: job.id,
                                            title: job.title,
                                            description: job.description,
                                            salary: job.salary,
                                            company_id: job.company_id,
                                        });
                                    }}>Edit</button>
                                    <button className="btn secondary" onClick={() => onDelete(job.id)}>Delete</button>
                                </div>
                            </>
                        )}
                    </article>
                ))}
            </div>
            <article className="entity-card form-card">
                <h3>Add Job</h3>
                <div className="entity-form">
                    <input type="text" value={addform.title} onChange={(e)=>setAddform({...addform,title:e.target.value})} placeholder="Title" />
                    <input type="text" value={addform.description} onChange={(e)=>setAddform({...addform,description:e.target.value})} placeholder="Description" />
                    <input type="text" value={addform.salary} onChange={(e)=>setAddform({...addform,salary:e.target.value})} placeholder="Salary" />
                    <input type="number" value={addform.company_id} onChange={(e)=>setAddform({...addform,company_id:Number(e.target.value)})} placeholder="Company ID" />
                    <button className="btn" onClick={handleAdd}>Add Job</button>
                </div>
            </article>
        </section>
    )
}

export default JobCard