import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation } from "@tanstack/react-query";
import { format } from "date-fns";
import api from "@/api/client";
import { accountSchema, type AccountFormValues } from "@/schemas/account";
import { type Account } from "@/types";
import { useToast } from "@/hooks/use-toast"; // Import Toast Hook

// UI Components
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"; // Import RadioGroup
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormDescription,
} from "@/components/ui/form";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";

// Icons & Utils
import { ArrowLeft, Trash2, Save, CalendarIcon } from "lucide-react";

// Options
const GENDER_OPTIONS = ["Male", "Female", "Other"];
const STATUS_OPTIONS = ["Active", "Inactive", "Closed"];
const SERVICE_OPTIONS = ["Internet Banking", "Debit Card", "Cheque Book", "SMS Alerts"];

export default function AccountDetailsPage() {
  const { accountId } = useParams();
  const navigate = useNavigate();
  const role = localStorage.getItem("role");
  const { toast } = useToast(); // Initialize Toast

  // 1. Fetch Data
  const {
    data: account,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["account", accountId],
    queryFn: async () => {
      const res = await api.get<Account>(`/accounts/${accountId}`);
      return res.data;
    },
    retry: false,
  });

  // 2. Loading / Error States
  if (isLoading) return <div className="p-20 text-center">Loading account details...</div>;
  if (isError || !account) return <div className="p-20 text-center text-destructive">Account not found</div>;

  // 3. Normalization Logic
  const normalize = (val: string | undefined, options: string[]) => {
    if (!val) return options[0];
    return options.find(o => o.toLowerCase() === val.toLowerCase()) || options[0];
  };

  const defaultValues: AccountFormValues = {
    account_holder_name: account.account_holder_name,
    dob: account.dob,
    email: account.email,
    phone: account.phone,
    address: account.address,
    zip_code: account.zip_code,
    balance: account.balance,
    marketing_opt_in: account.marketing_opt_in,
    services: account.services ? account.services.split(",") : [],

    // Normalized Values for Selects
    // @ts-ignore
    gender: normalize(account.gender, GENDER_OPTIONS),
    // @ts-ignore
    status: normalize(account.status, STATUS_OPTIONS),
    // @ts-ignore
    account_type: account.account_type
      ? account.account_type.charAt(0).toUpperCase() + account.account_type.slice(1).toLowerCase()
      : "Savings",

    agreed_to_terms: true,
  };

  return <AccountForm account={account} defaultValues={defaultValues} role={role} navigate={navigate} toast={toast} />;
}

// Separated Form Component
function AccountForm({
  account,
  defaultValues,
  role,
  navigate,
  toast
}: {
  account: Account,
  defaultValues: AccountFormValues,
  role: string | null,
  navigate: any,
  toast: any
}) {
  const form = useForm<AccountFormValues>({
    resolver: zodResolver(accountSchema),
    defaultValues,
  });

  const [isCalendarOpen, setIsCalendarOpen] = useState(false);

  const updateMutation = useMutation({
    mutationFn: async (values: AccountFormValues) => {
      const payload = { ...values, services: values.services?.join(",") || "" };
      await api.put(`/accounts/${account.account_id}`, payload);
    },
    onSuccess: () => {
      // SUCCESS TOAST
      toast({
        title: "Changes Saved",
        description: "Account details have been successfully updated.",
        variant: "default", // or just omit for default style
        className: "bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-900", // Optional custom styling
      });
    },
    onError: () => {
      // ERROR TOAST
      toast({
        title: "Update Failed",
        description: "There was a problem saving your changes. Please try again.",
        variant: "destructive",
      });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async () => {
      await api.delete(`/accounts/${account.account_id}`);
    },
    onSuccess: () => {
      toast({
        title: "Account Deleted",
        description: `Account ${account.account_id} has been permanently removed.`,
      });
      navigate("/dashboard");
    },
    onError: () => {
      toast({
        title: "Deletion Failed",
        description: "Could not delete this account. You may lack permissions.",
        variant: "destructive",
      });
    },
  });

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-20">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="outline" size="icon" onClick={() => navigate("/dashboard")}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
              Account Details
              <Badge variant={account.status === "Active" ? "default" : "secondary"}>
                {account.status}
              </Badge>
            </h1>
            <p className="text-muted-foreground font-mono">ID: {account.account_id}</p>
          </div>
        </div>

        {role === "manager" && (
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button variant="destructive">
                <Trash2 className="mr-2 h-4 w-4" /> Delete Account
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Delete this account?</AlertDialogTitle>
                <AlertDialogDescription>
                  This will permanently delete <strong>{account.account_holder_name}'s</strong> account.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction onClick={() => deleteMutation.mutate()} className="bg-destructive text-destructive-foreground">
                  Delete Account
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        )}
      </div>

      <Form {...form}>
        <form onSubmit={form.handleSubmit((v) => updateMutation.mutate(v))} className="space-y-8">

          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Personal Information</CardTitle>
                <CardDescription>Identity details</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <FormField control={form.control} name="account_holder_name" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Full Name</FormLabel>
                    <FormControl><Input {...field} /></FormControl>
                    <FormMessage />
                  </FormItem>
                )} />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* items-end ensures if labels differ in height, inputs still align bottom */}

                  {/* --- HYBRID DATE INPUT --- */}
                  <FormField
                    control={form.control}
                    name="dob"
                    render={({ field }) => (
                      <FormItem className="flex flex-col">
                        <FormLabel>Date of Birth</FormLabel>
                        <div className="relative">
                          {/* 1. Manual Input with EXACT Height & Padding */}
                          <FormControl>
                            <Input
                                placeholder="YYYY-MM-DD"
                                {...field}
                                className="h-10 pr-10 block w-full"
                            />
                          </FormControl>

                          {/* 2. Calendar Trigger Icon */}
                          <Popover open={isCalendarOpen} onOpenChange={setIsCalendarOpen}>
                            <PopoverTrigger asChild>
                              <Button
                                variant="ghost"
                                size="icon"
                                className="absolute right-0 top-0 h-10 w-10" // Matches Input Height
                                type="button"
                              >
                                <CalendarIcon className="h-4 w-4 text-muted-foreground" />
                              </Button>
                            </PopoverTrigger>
                            <PopoverContent className="w-auto p-0" align="end">
                              <Calendar
                                mode="single"
                                selected={field.value ? new Date(field.value) : undefined}
                                defaultMonth={field.value ? new Date(field.value) : undefined}
                                onSelect={(date) => {
                                  if (date) {
                                    field.onChange(format(date, "yyyy-MM-dd"));
                                    setIsCalendarOpen(false);
                                  }
                                }}
                                disabled={(date) => date > new Date() || date < new Date("1900-01-01")}
                                captionLayout="dropdown-buttons"
                                fromYear={1900}
                                toYear={new Date().getFullYear()}
                                initialFocus
                              />
                            </PopoverContent>
                          </Popover>
                        </div>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  {/* --- GENDER RADIO BUTTONS --- */}
                  <FormField
                    control={form.control}
                    name="gender"
                    render={({ field }) => (
                      <FormItem className="space-y-3">
                        <FormLabel>Gender</FormLabel>
                        <FormControl>
                          <RadioGroup
                            onValueChange={field.onChange}
                            defaultValue={field.value}
                            className="flex flex-col space-y-1"
                          >
                            {GENDER_OPTIONS.map((opt) => (
                              <FormItem key={opt} className="flex items-center space-x-3 space-y-0">
                                <FormControl>
                                  <RadioGroupItem value={opt} />
                                </FormControl>
                                <FormLabel className="font-normal">
                                  {opt}
                                </FormLabel>
                              </FormItem>
                            ))}
                          </RadioGroup>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Contact Information</CardTitle>
                <CardDescription>Communication details</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <FormField control={form.control} name="email" render={({ field }) => (
                    <FormItem>
                      <FormLabel>Email</FormLabel>
                      <FormControl><Input {...field} /></FormControl>
                      <FormMessage />
                    </FormItem>
                  )} />
                  <FormField control={form.control} name="phone" render={({ field }) => (
                    <FormItem>
                      <FormLabel>Phone</FormLabel>
                      <FormControl><Input {...field} /></FormControl>
                      <FormMessage />
                    </FormItem>
                  )} />
                </div>
                <FormField control={form.control} name="address" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Address</FormLabel>
                    <FormControl><Input {...field} /></FormControl>
                    <FormMessage />
                  </FormItem>
                )} />
                <FormField control={form.control} name="zip_code" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Zip Code</FormLabel>
                    <FormControl><Input {...field} /></FormControl>
                    <FormMessage />
                  </FormItem>
                )} />
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Account Status & Services</CardTitle>
              <CardDescription>Manage account properties</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-3 gap-6">

                {/* Account Type (Disabled) */}
                <FormField control={form.control} name="account_type" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Account Type</FormLabel>
                    <FormControl>
                        <Input {...field} disabled className="bg-muted font-semibold text-muted-foreground h-10" />
                    </FormControl>
                    <FormDescription className="text-xs">Cannot be changed.</FormDescription>
                  </FormItem>
                )} />

                {/* Account Status */}
                <FormField control={form.control} name="status" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Account Status</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                          <SelectTrigger className="h-10">
                              <SelectValue placeholder="Select" />
                          </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                         {STATUS_OPTIONS.map(opt => (
                             <SelectItem key={opt} value={opt}>{opt}</SelectItem>
                         ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )} />

                <FormField control={form.control} name="balance" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Current Balance ($)</FormLabel>
                    <FormControl><Input type="number" step="0.01" {...field} className="h-10" /></FormControl>
                    <FormMessage />
                  </FormItem>
                )} />
              </div>

              <Separator />

              <FormField control={form.control} name="services" render={() => (
                <FormItem>
                  <FormLabel className="text-base">Active Services</FormLabel>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-2">
                    {SERVICE_OPTIONS.map((item) => (
                      <FormField key={item} control={form.control} name="services" render={({ field }) => (
                        <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                          <FormControl>
                            <Checkbox
                              checked={field.value?.includes(item)}
                              onCheckedChange={(checked) => {
                                return checked
                                  ? field.onChange([...(field.value || []), item])
                                  : field.onChange(field.value?.filter((value) => value !== item))
                              }}
                            />
                          </FormControl>
                          <FormLabel className="font-normal cursor-pointer">{item}</FormLabel>
                        </FormItem>
                      )} />
                    ))}
                  </div>
                </FormItem>
              )} />

              <Separator />

              <FormField control={form.control} name="marketing_opt_in" render={({ field }) => (
                <FormItem className="flex flex-row items-center space-x-3 space-y-0 p-4 border rounded-md bg-muted/20">
                  <FormControl>
                    <Checkbox checked={field.value} onCheckedChange={field.onChange} />
                  </FormControl>
                  <div className="space-y-1 leading-none">
                    <FormLabel>Marketing Communications</FormLabel>
                    <FormDescription>Customer has agreed to receive updates via email.</FormDescription>
                  </div>
                </FormItem>
              )} />

              <FormField control={form.control} name="agreed_to_terms" render={({ field }) => (
                   <input type="hidden" {...field} value="true" />
              )} />

            </CardContent>
          </Card>

          <div className="flex justify-end gap-4 sticky bottom-0 bg-background/95 backdrop-blur py-4 border-t z-10">
             <Button type="button" variant="outline" onClick={() => navigate("/dashboard")}>
                Cancel
             </Button>
             <Button type="submit" size="lg" className="min-w-[150px]" disabled={updateMutation.isPending}>
                <Save className="mr-2 h-4 w-4" />
                {updateMutation.isPending ? "Saving..." : "Save Changes"}
             </Button>
          </div>

        </form>
      </Form>
    </div>
  );
}