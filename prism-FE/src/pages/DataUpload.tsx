import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Upload, FileText, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const DataUpload = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const { toast } = useToast();

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      toast({
        title: "File selected",
        description: `${file.name} ready to upload`,
      });
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsUploading(true);
    
    // Simulate upload
    setTimeout(() => {
      setIsUploading(false);
      toast({
        title: "Upload successful",
        description: "Data processed and ready for forecasting",
      });
    }, 2000);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Data Upload</h1>
        <p className="text-muted-foreground mt-2">Upload historical data or enter project details manually</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* CSV Upload */}
        <Card>
          <CardHeader>
            <CardTitle>Upload CSV File</CardTitle>
            <CardDescription>Upload historical procurement data for analysis</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary transition-colors cursor-pointer">
              <input
                type="file"
                accept=".csv"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <Upload className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                {uploadedFile ? (
                  <div className="space-y-2">
                    <div className="flex items-center justify-center gap-2 text-success">
                      <FileText className="h-5 w-5" />
                      <span className="font-medium">{uploadedFile.name}</span>
                    </div>
                    <p className="text-sm text-muted-foreground">Click to change file</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <p className="text-foreground font-medium">Drop your CSV file here</p>
                    <p className="text-sm text-muted-foreground">or click to browse</p>
                  </div>
                )}
              </label>
            </div>
            {uploadedFile && (
              <Button onClick={handleSubmit} className="w-full mt-4" disabled={isUploading}>
                {isUploading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  "Upload and Process"
                )}
              </Button>
            )}
          </CardContent>
        </Card>

        {/* Manual Entry Form */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Forecast Mode</CardTitle>
            <CardDescription>Enter project details for instant forecasting</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="project-type">Project Type</Label>
                <Select>
                  <SelectTrigger id="project-type">
                    <SelectValue placeholder="Select project type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="transmission">Transmission Line</SelectItem>
                    <SelectItem value="substation">Substation</SelectItem>
                    <SelectItem value="distribution">Distribution Network</SelectItem>
                    <SelectItem value="generation">Power Generation</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="location">Location</Label>
                <Input id="location" placeholder="e.g., Mumbai, Maharashtra" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="duration">Duration (months)</Label>
                <Input id="duration" type="number" placeholder="12" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="budget">Budget (₹ Lakhs)</Label>
                <Input id="budget" type="number" placeholder="5000" />
              </div>

              <Button type="submit" className="w-full" disabled={isUploading}>
                {isUploading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Forecast...
                  </>
                ) : (
                  "Generate Forecast"
                )}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default DataUpload;
