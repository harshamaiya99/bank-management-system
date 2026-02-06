export interface User {
  username: string;
  role: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  role: string;
}

export interface Account {
  account_id: string;
  account_holder_name: string;
  dob: string;
  gender: string;
  email: string;
  phone: string;
  address: string;
  zip_code: string;
  account_type: string;
  balance: number;
  date_opened: string;
  status: string;
  services: string;
  marketing_opt_in: boolean;
  agreed_to_terms: boolean;
}

export interface CreateAccountPayload {
  account_holder_name: string;
  dob: string;
  gender: string;
  email: string;
  phone: string;
  address: string;
  zip_code: string;
  account_type: string;
  balance: number;
  status: string;
  services: string;
  marketing_opt_in: boolean;
  agreed_to_terms: boolean;
}