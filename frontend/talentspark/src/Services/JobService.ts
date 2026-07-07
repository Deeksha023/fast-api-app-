import api from "./api"
import type { Job } from "../types/job"

function toJobPayload(job: Job) {
    const companyName = job.company_name?.trim()

    return {
        title: job.title,
        description: job.description,
        salary: Number(job.salary),
        company_id: companyName ? undefined : job.company_id,
        company_name: companyName || undefined,
    }
}

function fromApiJob(job: Omit<Job, "salary"> & { salary: number }): Job {
    return {
        ...job,
        salary: String(job.salary),
        company_name: "",
    }
}

export async function getJobs(): Promise<Job[]> {
    const response = await api.get("/job/")
    return response.data.map(fromApiJob)
}

export async function getJob(id: number): Promise<Job> {
    const response = await api.get(`/job/${id}`)
    return fromApiJob(response.data)
}

export async function createJob(job: Job): Promise<Job> {
    const response = await api.post("/job/", toJobPayload(job))
    return fromApiJob(response.data)
}

export async function updateJob(id: number, job: Job): Promise<Job> {
    const response = await api.put(`/job/${id}`, toJobPayload(job))
    return fromApiJob(response.data)
}

export async function deleteJob(id: number): Promise<void> {
    const response = await api.delete(`/job/${id}`)
    return response.data
}
