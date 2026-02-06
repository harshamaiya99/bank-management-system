import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "@/api/client";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search, PlusCircle, ArrowRight } from "lucide-react";

export default function DashboardPage() {
  const navigate = useNavigate();
  const [searchId, setSearchId] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchId || searchId.length !== 7) {
      setError("Please enter a valid 7-digit Account ID");
      return;
    }

    setLoading(true);
    setError("");

    try {
      // Quick check if account exists before navigating
      await api.get(`/accounts/${searchId}`);
      navigate(`/account-details/${searchId}`);
    } catch (err: any) {
      if (err.response?.status === 404) {
        setError("Account not found.");
      } else {
        setError("An error occurred. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 mt-10">
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">Manage accounts and customer services</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Search Card */}
        <Card>
          <CardHeader>
            <CardTitle>Find Account</CardTitle>
            <CardDescription>Search for an existing customer account</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSearch} className="space-y-4">
              <div className="space-y-2">
                <Input
                  placeholder="Enter 7-digit Account ID"
                  value={searchId}
                  onChange={(e) => setSearchId(e.target.value)}
                  maxLength={7}
                />
                {error && <p className="text-sm text-destructive">{error}</p>}
              </div>
              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? "Searching..." : (
                  <>
                    <Search className="mr-2 h-4 w-4" /> Search Account
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Create Card */}
        <Card className="flex flex-col justify-between">
          <CardHeader>
            <CardTitle>Open New Account</CardTitle>
            <CardDescription>Register a new customer account</CardDescription>
          </CardHeader>
          <CardContent className="mt-auto">
            <Button
              variant="default"
              className="w-full bg-green-600 hover:bg-green-700"
              onClick={() => navigate("/create-account")}
            >
              <PlusCircle className="mr-2 h-4 w-4" /> Create Account
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}