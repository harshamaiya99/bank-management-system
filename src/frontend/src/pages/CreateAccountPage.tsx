import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { format } from "date-fns";
import api from "@/api/client";
import { accountSchema, type AccountFormValues } from "@/schemas/account";
import { useToast } from "@/hooks/use-toast";

// Components
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";

// Icons
import { ArrowLeft, CalendarIcon } from "lucide-react";

const servicesOptions = ["Internet Banking", "Debit Card", "Cheque Book", "SMS Alerts"];

export default function CreateAccountPage() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);

  const form = useForm<AccountFormValues>({
    resolver: zodResolver(accountSchema),
    defaultValues: {
      account_holder_name: "",
      balance: 0,
      marketing_opt_in: false,
      services: [],
      status: "Active",
      agreed_to_terms: false,
    },
  });

  const createMutation = useMutation({
    mutationFn: async (values: AccountFormValues) => {
      const payload = { ...values, services: values.services?.join(",") || "" };
      const res = await api.post("/accounts", payload, {
        headers: { "Idempotency-Id": crypto.randomUUID() },
      });
      return res.data;
    },
    // FIX: Add 'variables' to access the form data we just sent
    onSuccess: (data, variables) => {
      toast({
        title: "Account Opened",
        // FIX: Use 'variables.account_holder_name' to guarantee the name shows up
        description: `Successfully created account ${data.account_id} for ${variables.account_holder_name}`,
        className: "bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-900",
      });
      navigate(`/account-details/${data.account_id}`);
    },
    onError: () => {
      toast({
        title: "Application Failed",
        description: "Could not create the account. Please verify the input details.",
        variant: "destructive",
      });
    },
  });

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-20">
      <div className="flex items-center gap-4">
        <Button variant="outline" size="icon" onClick={() => navigate("/dashboard")}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">New Account Application</h1>
          <p className="text-muted-foreground">Enter customer details to open a new banking account.</p>
        </div>
      </div>

      <Form {...form}>
        <form onSubmit={form.handleSubmit((v) => createMutation.mutate(v))} className="space-y-8">

          <div className="grid gap-6 md:grid-cols-2">
            {/* Personal Details Card */}
            <Card>
              <CardHeader>
                <CardTitle>Personal Information</CardTitle>
                <CardDescription>Identity details of the account holder</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <FormField control={form.control} name="account_holder_name" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Full Name</FormLabel>
                    <FormControl><Input placeholder="Jane Doe" {...field} /></FormControl>
                    <FormMessage />
                  </FormItem>
                )} />

                <div className="grid grid-cols-2 gap-4 items-end">

                    {/* --- HYBRID DATE INPUT --- */}
                    <FormField
                    control={form.control}
                    name="dob"
                    render={({ field }) => (
                      <FormItem className="flex flex-col">
                        <FormLabel>Date of Birth</FormLabel>
                        <div className="relative">
                          {/* 1. Manual Input */}
                          <FormControl>
                            <Input
                                placeholder="YYYY-MM-DD"
                                {...field}
                                className="h-10 pr-10 block w-full"
                            />
                          </FormControl>

                          {/* 2. Calendar Popover */}
                          <Popover open={isCalendarOpen} onOpenChange={setIsCalendarOpen}>
                            <PopoverTrigger asChild>
                              <Button
                                variant="ghost"
                                size="icon"
                                className="absolute right-0 top-0 h-10 w-10 text-muted-foreground hover:text-foreground"
                                type="button"
                              >
                                <CalendarIcon className="h-4 w-4" />
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

                    <FormField control={form.control} name="gender" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Gender</FormLabel>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                            <FormControl>
                                {/* Force exact height match */}
                                <SelectTrigger className="h-10 w-full">
                                    <SelectValue placeholder="Select" />
                                </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                                <SelectItem value="Male">Male</SelectItem>
                                <SelectItem value="Female">Female</SelectItem>
                                <SelectItem value="Other">Other</SelectItem>
                            </SelectContent>
                        </Select>
                        <FormMessage />
                    </FormItem>
                    )} />
                </div>
              </CardContent>
            </Card>

            {/* Contact Details Card */}
            <Card>
              <CardHeader>
                <CardTitle>Contact Information</CardTitle>
                <CardDescription>Address and communication details</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                    <FormField control={form.control} name="email" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Email</FormLabel>
                        <FormControl><Input placeholder="name@example.com" {...field} /></FormControl>
                        <FormMessage />
                    </FormItem>
                    )} />
                    <FormField control={form.control} name="phone" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Phone</FormLabel>
                        <FormControl><Input placeholder="+1 234 567 890" {...field} /></FormControl>
                        <FormMessage />
                    </FormItem>
                    )} />
                </div>
                <FormField control={form.control} name="address" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Address</FormLabel>
                    <FormControl><Input placeholder="123 Street Name" {...field} /></FormControl>
                    <FormMessage />
                  </FormItem>
                )} />
                <FormField control={form.control} name="zip_code" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Zip Code</FormLabel>
                    <FormControl><Input placeholder="10001" {...field} /></FormControl>
                    <FormMessage />
                  </FormItem>
                )} />
              </CardContent>
            </Card>
          </div>

          {/* Account Settings Card */}
          <Card>
            <CardHeader>
              <CardTitle>Account Configuration</CardTitle>
              <CardDescription>Set up account type and initial services</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-6">
                <FormField control={form.control} name="account_type" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Account Type</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                          <SelectTrigger className="h-10">
                              <SelectValue placeholder="Select Type" />
                          </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="Savings">Savings</SelectItem>
                        <SelectItem value="Current">Current</SelectItem>
                        <SelectItem value="Salary">Salary</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )} />
                <FormField control={form.control} name="balance" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Initial Deposit ($)</FormLabel>
                    <FormControl><Input type="number" step="0.01" {...field} className="h-10" /></FormControl>
                    <FormMessage />
                  </FormItem>
                )} />
              </div>

              <Separator />

              <FormField control={form.control} name="services" render={() => (
                <FormItem>
                  <FormLabel className="text-base">Banking Services</FormLabel>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-2">
                    {servicesOptions.map((item) => (
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
                <FormItem className="flex flex-row items-start space-x-3 space-y-0 ">
                  <FormControl>
                    <Checkbox checked={field.value} onCheckedChange={field.onChange} />
                  </FormControl>
                  <div className="space-y-1 leading-none">
                    <FormLabel>Marketing Communications</FormLabel>
                    <FormDescription>
                      Customer agrees to receive updates, offers, and news via email.
                    </FormDescription>
                  </div>
                </FormItem>
              )} />
            </CardContent>
          </Card>

          {/* Terms & Privacy Card */}

            <CardContent className="space-y-6">
              <FormField control={form.control} name="agreed_to_terms" render={({ field }) => (
                <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                  <FormControl>
                    <Checkbox checked={field.value} onCheckedChange={field.onChange} />
                  </FormControl>
                  <div className="space-y-1 leading-none">
                    <FormLabel>Terms and Conditions</FormLabel>
                    <FormDescription>
                      I verify that the customer has read and agreed to the bank's terms of service and privacy policy.
                    </FormDescription>
                    <FormMessage />
                  </div>
                </FormItem>
              )} />
            </CardContent>


          {/* Submit Actions */}
          <div className="flex justify-end gap-4">
             <Button type="button" variant="ghost" onClick={() => navigate("/dashboard")}>Cancel</Button>
             <Button type="submit" size="lg" className="min-w-[150px]" disabled={createMutation.isPending}>
                {createMutation.isPending ? "Creating..." : "Create Account"}
             </Button>
          </div>
        </form>
      </Form>
    </div>
  );
}