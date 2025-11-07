import { useState, useEffect } from "react";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Upload, FileText, Loader2, CheckCircle, AlertCircle, Database, Sparkles, Info } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import GradientCard from "@/components/GradientCard";
import GradientButton from "@/components/GradientButton";
import GlowInput from "@/components/GlowInput";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

const existingSchemas = [
  { id: "schema1", name: "Q1 2024 Materials", fields: 7, lastUsed: "2024-03-15", records: 1250 },
  { id: "schema2", name: "Infrastructure Projects", fields: 8, lastUsed: "2024-02-28", records: 890 },
  { id: "schema3", name: "Supplier Database", fields: 6, lastUsed: "2024-01-10", records: 2100 },
];

const requiredFields = [
  { name: "project_id", description: "Unique identifier for the project" },
  { name: "material", description: "Name or type of material" },
  { name: "quantity", description: "Amount of material required" },
  { name: "unit_cost", description: "Cost per unit of material" },
  { name: "date", description: "Date of procurement or forecast" },
  { name: "location", description: "Project or delivery location" },
  { name: "supplier", description: "Supplier name or ID" },
];

const DataUpload = () => {
  const [uploadMode, setUploadMode] = useState<"new" | "existing">("new");
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [selectedSchema, setSelectedSchema] = useState("");
  const [animateIn, setAnimateIn] = useState(false);
  const [uploadStep, setUploadStep] = useState<"idle" | "uploading" | "validating" | "processing" | "complete">("idle");
  const { toast } = useToast();

  useEffect(() => {
    const timer = setTimeout(() => setAnimateIn(true), 100);
    return () => clearTimeout(timer);
  }, []);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.name.endsWith(".csv")) {
        toast({
          title: "Invalid file type",
          description: "Please upload a CSV file",
          variant: "destructive",
        });
        return;
      }
      setUploadedFile(file);
      toast({
        title: "File selected",
        description: `${file.name} ready to upload`,
      });
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadedFile) return;

    setIsUploading(true);
    setUploadStep("uploading");
    setUploadProgress(0);

    // Simulate upload progress
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setUploadStep("validating");
          setTimeout(() => {
            setUploadStep("processing");
            setTimeout(() => {
              setUploadStep("complete");
              setIsUploading(false);
              toast({
                title: "Upload successful!",
                description: uploadMode === "new" 
                  ? "New schema created and data processed successfully"
                  : "Data uploaded to existing schema successfully",
              });
            }, 1500);
          }, 1500);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const getStepStatus = (step: string) => {
    const steps = ["uploading", "validating", "processing", "complete"];
    const currentIndex = steps.indexOf(uploadStep);
    const stepIndex = steps.indexOf(step);
    
    if (stepIndex < currentIndex) return "complete";
    if (stepIndex === currentIndex) return "active";
    return "pending";
  };

  return (
    <div className="min-h-screen pb-8 space-y-6">
      {/* Header */}
      <div
        className={`fade-in-up ${animateIn ? "opacity-100" : "opacity-0"}`}
      >
        <div className="flex items-center gap-4 mb-2">
          <div className="h-14 w-14 rounded-2xl bg-purple-gradient flex items-center justify-center shadow-lg glow-purple">
            <Upload className="h-7 w-7 text-white" />
          </div>
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent">
              Data Upload
            </h1>
            <p className="text-muted-foreground mt-1">
              Upload historical data or create new schema for forecasting
            </p>
          </div>
        </div>
      </div>

      {/* Toggle Selector */}
      <div
        className={`fade-in-up stagger-1 ${animateIn ? "opacity-100" : "opacity-0"}`}
      >
        <GradientCard variant="glass" className="border-2 border-border/50">
          <div className="p-6">
            <div className="flex items-center justify-center gap-4">
              <button
                onClick={() => setUploadMode("new")}
                className={`flex-1 p-6 rounded-xl border-2 transition-all duration-300 ${
                  uploadMode === "new"
                    ? "border-teal-500 bg-teal-500/10 shadow-lg glow-teal"
                    : "border-border/50 hover:border-border"
                }`}
              >
                <div className="flex flex-col items-center gap-3">
                  <div className={`h-16 w-16 rounded-2xl flex items-center justify-center ${
                    uploadMode === "new" ? "bg-teal-gradient" : "bg-muted"
                  }`}>
                    <Sparkles className={`h-8 w-8 ${uploadMode === "new" ? "text-white" : "text-muted-foreground"}`} />
                  </div>
                  <div className="text-center">
                    <h3 className="font-semibold text-lg text-foreground">New Schema Upload</h3>
                    <p className="text-sm text-muted-foreground mt-1">
                      Upload a completely new CSV schema
                    </p>
                  </div>
                </div>
              </button>

              <button
                onClick={() => setUploadMode("existing")}
                className={`flex-1 p-6 rounded-xl border-2 transition-all duration-300 ${
                  uploadMode === "existing"
                    ? "border-purple-500 bg-purple-500/10 shadow-lg glow-purple"
                    : "border-border/50 hover:border-border"
                }`}
              >
                <div className="flex flex-col items-center gap-3">
                  <div className={`h-16 w-16 rounded-2xl flex items-center justify-center ${
                    uploadMode === "existing" ? "bg-purple-gradient" : "bg-muted"
                  }`}>
                    <Database className={`h-8 w-8 ${uploadMode === "existing" ? "text-white" : "text-muted-foreground"}`} />
                  </div>
                  <div className="text-center">
                    <h3 className="font-semibold text-lg text-foreground">Existing Schema Upload</h3>
                    <p className="text-sm text-muted-foreground mt-1">
                      Upload data using a previously trained schema
                    </p>
                  </div>
                </div>
              </button>
            </div>
          </div>
        </GradientCard>
      </div>

      {/* Dynamic Form */}
      <div
        className={`fade-in-up stagger-2 ${animateIn ? "opacity-100" : "opacity-0"}`}
      >
        {uploadMode === "new" ? (
          <GradientCard
            variant="teal"
            title="New Schema Upload"
            description="Create a new schema by uploading a CSV file with the required fields"
            className="border-2 border-teal-500/20"
          >
            {/* Required Fields Info */}
            <div className="mb-6 p-4 rounded-lg bg-teal-500/5 border border-teal-500/20">
              <div className="flex items-start gap-3">
                <Info className="h-5 w-5 text-teal-600 mt-0.5" />
                <div className="flex-1">
                  <h4 className="font-medium text-foreground mb-2">Required Fields</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {requiredFields.map((field) => (
                      <TooltipProvider key={field.name}>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <div className="flex items-center gap-2 text-sm">
                              <Badge variant="outline" className="font-mono">
                                {field.name}
                              </Badge>
                            </div>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>{field.description}</p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* File Upload Zone */}
            <div
              className={`border-2 border-dashed rounded-xl p-12 text-center transition-all duration-300 ${
                uploadedFile
                  ? "border-teal-500 bg-teal-500/5"
                  : "border-border hover:border-teal-500 hover:bg-teal-500/5"
              } cursor-pointer group`}
            >
              <input
                type="file"
                accept=".csv"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload-new"
              />
              <label htmlFor="file-upload-new" className="cursor-pointer">
                {uploadedFile ? (
                  <div className="space-y-3">
                    <div className="h-16 w-16 mx-auto rounded-2xl bg-teal-gradient flex items-center justify-center">
                      <FileText className="h-8 w-8 text-white" />
                    </div>
                    <div>
                      <p className="font-semibold text-foreground text-lg">{uploadedFile.name}</p>
                      <p className="text-sm text-muted-foreground mt-1">
                        {(uploadedFile.size / 1024).toFixed(2)} KB
                      </p>
                    </div>
                    <p className="text-sm text-teal-600">Click to change file</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <div className="h-16 w-16 mx-auto rounded-2xl bg-muted group-hover:bg-teal-500/10 flex items-center justify-center transition-colors">
                      <Upload className="h-8 w-8 text-muted-foreground group-hover:text-teal-600 transition-colors" />
                    </div>
                    <div>
                      <p className="font-semibold text-foreground text-lg">Drop your CSV file here</p>
                      <p className="text-sm text-muted-foreground mt-1">or click to browse</p>
                    </div>
                  </div>
                )}
              </label>
            </div>

            {uploadedFile && (
              <div className="mt-6">
                <GradientButton
                  onClick={handleSubmit}
                  variant="teal"
                  className="w-full h-12 text-base font-semibold"
                  disabled={isUploading}
                >
                  {isUploading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <Sparkles className="mr-2 h-5 w-5" />
                      Upload & Train New Schema
                    </>
                  )}
                </GradientButton>
              </div>
            )}
          </GradientCard>
        ) : (
          <GradientCard
            variant="purple"
            title="Existing Schema Upload"
            description="Select a previously trained schema and upload your data"
            className="border-2 border-purple-500/20"
          >
            {/* Schema Selector */}
            <div className="mb-6">
              <Label htmlFor="schema-select" className="text-sm font-medium mb-2 block">
                Select Schema
              </Label>
              <Select value={selectedSchema} onValueChange={setSelectedSchema}>
                <SelectTrigger id="schema-select" className="h-12">
                  <SelectValue placeholder="Choose an existing schema" />
                </SelectTrigger>
                <SelectContent>
                  {existingSchemas.map((schema) => (
                    <SelectItem key={schema.id} value={schema.id}>
                      <div className="flex items-center justify-between w-full">
                        <span className="font-medium">{schema.name}</span>
                        <Badge variant="outline" className="ml-2">
                          {schema.fields} fields
                        </Badge>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              {selectedSchema && (
                <div className="mt-4 p-4 rounded-lg bg-purple-500/5 border border-purple-500/20">
                  {existingSchemas
                    .filter((s) => s.id === selectedSchema)
                    .map((schema) => (
                      <div key={schema.id} className="grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <p className="text-muted-foreground">Fields</p>
                          <p className="font-semibold text-foreground">{schema.fields}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Last Used</p>
                          <p className="font-semibold text-foreground">{schema.lastUsed}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Records</p>
                          <p className="font-semibold text-foreground">{schema.records.toLocaleString()}</p>
                        </div>
                      </div>
                    ))}
                </div>
              )}
            </div>

            {/* File Upload Zone */}
            <div
              className={`border-2 border-dashed rounded-xl p-12 text-center transition-all duration-300 ${
                uploadedFile
                  ? "border-purple-500 bg-purple-500/5"
                  : "border-border hover:border-purple-500 hover:bg-purple-500/5"
              } cursor-pointer group`}
            >
              <input
                type="file"
                accept=".csv"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload-existing"
              />
              <label htmlFor="file-upload-existing" className="cursor-pointer">
                {uploadedFile ? (
                  <div className="space-y-3">
                    <div className="h-16 w-16 mx-auto rounded-2xl bg-purple-gradient flex items-center justify-center">
                      <FileText className="h-8 w-8 text-white" />
                    </div>
                    <div>
                      <p className="font-semibold text-foreground text-lg">{uploadedFile.name}</p>
                      <p className="text-sm text-muted-foreground mt-1">
                        {(uploadedFile.size / 1024).toFixed(2)} KB
                      </p>
                    </div>
                    <p className="text-sm text-purple-600">Click to change file</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <div className="h-16 w-16 mx-auto rounded-2xl bg-muted group-hover:bg-purple-500/10 flex items-center justify-center transition-colors">
                      <Upload className="h-8 w-8 text-muted-foreground group-hover:text-purple-600 transition-colors" />
                    </div>
                    <div>
                      <p className="font-semibold text-foreground text-lg">Drop your CSV file here</p>
                      <p className="text-sm text-muted-foreground mt-1">or click to browse</p>
                    </div>
                  </div>
                )}
              </label>
            </div>

            {uploadedFile && selectedSchema && (
              <div className="mt-6">
                <GradientButton
                  onClick={handleSubmit}
                  variant="purple"
                  className="w-full h-12 text-base font-semibold"
                  disabled={isUploading}
                >
                  {isUploading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <Database className="mr-2 h-5 w-5" />
                      Upload to Existing Schema
                    </>
                  )}
                </GradientButton>
              </div>
            )}
          </GradientCard>
        )}
      </div>

      {/* Progress Indicator */}
      {isUploading && (
        <GradientCard
          variant="glass"
          className={`border-2 border-border/50 fade-in-up`}
        >
          <div className="space-y-6">
            <div>
              <div className="flex items-center justify-between mb-2">
                <p className="text-sm font-medium text-foreground">Upload Progress</p>
                <p className="text-sm font-medium text-foreground">{uploadProgress}%</p>
              </div>
              <Progress value={uploadProgress} className="h-2" />
            </div>

            <div className="grid grid-cols-4 gap-4">
              {["uploading", "validating", "processing", "complete"].map((step) => {
                const status = getStepStatus(step);
                return (
                  <div key={step} className="text-center">
                    <div
                      className={`h-12 w-12 mx-auto rounded-full flex items-center justify-center mb-2 transition-all duration-300 ${
                        status === "complete"
                          ? "bg-green-500 text-white"
                          : status === "active"
                          ? "bg-teal-gradient text-white animate-pulse"
                          : "bg-muted text-muted-foreground"
                      }`}
                    >
                      {status === "complete" ? (
                        <CheckCircle className="h-6 w-6" />
                      ) : (
                        <Loader2 className={`h-6 w-6 ${status === "active" ? "animate-spin" : ""}`} />
                      )}
                    </div>
                    <p className="text-xs font-medium text-foreground capitalize">{step}</p>
                  </div>
                );
              })}
            </div>
          </div>
        </GradientCard>
      )}
    </div>
  );
};

export default DataUpload;

