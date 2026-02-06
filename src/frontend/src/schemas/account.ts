import * as z from "zod";

export const accountSchema = z.object({
  account_holder_name: z.string().min(2, "Name must be at least 2 characters"),
  dob: z.string().refine((val) => !isNaN(Date.parse(val)), "Invalid Date"),
  gender: z.enum(["Male", "Female", "Other"]),
  email: z.string().email(),
  phone: z.string().min(10, "Phone number too short"),
  address: z.string().min(5, "Address too short"),
  zip_code: z.string().min(4, "Invalid Zip Code"),
  account_type: z.enum(["Savings", "Current", "Salary"]),
  balance: z.coerce.number().min(0),
  status: z.enum(["Active", "Inactive", "Closed"]).optional().default("Active"),
  services: z.array(z.string()).optional(),
  marketing_opt_in: z.boolean().default(false),
  agreed_to_terms: z.literal(true, {
    errorMap: () => ({ message: "You must agree to the terms" }),
  }),
});

export type AccountFormValues = z.infer<typeof accountSchema>;