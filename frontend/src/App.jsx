import React, { useState } from 'react'
import config from './config'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Upload, FileText, Download, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import './App.css'

function App() {
  // State management
  const [currentStep, setCurrentStep] = useState(0)
  const [isProcessing, setIsProcessing] = useState(false)
  const [file, setFile] = useState(null)
  const [googleDocUrl, setGoogleDocUrl] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [region, setRegion] = useState('US')
  const [seniority, setSeniority] = useState('mid')
  const [tone, setTone] = useState('standard')
  const [resumeData, setResumeData] = useState(null)
  const [optimizedData, setOptimizedData] = useState(null)
  const [texString, setTexString] = useState('')
  const [error, setError] = useState('')
  const [progress, setProgress] = useState(0)

  const steps = [
    'Upload Resume',
    'Configure Options',
    'AI Optimization',
    'Generate PDF',
    'Download Results'
  ]

  const handleFileUpload = (event) => {
    const selectedFile = event.target.files[0]
    if (selectedFile) {
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']
      if (allowedTypes.includes(selectedFile.type)) {
        setFile(selectedFile)
        setError('')
      } else {
        setError('Please upload a PDF or DOCX file')
      }
    }
  }

  const ingestResume = async () => {
    setIsProcessing(true)
    setError('')
    setProgress(20)

    try {
      const formData = new FormData()
      
      if (file) {
        formData.append('file', file)
      } else if (googleDocUrl) {
        // Send as JSON for Google Docs URL
        const response = await fetch(`${config.getApiUrl()}/api/resume/ingest`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ googleDocUrl })
        })
        
        if (!response.ok) {
          throw new Error('Failed to ingest resume')
        }
        
        const data = await response.json()
        setResumeData(data)
        setProgress(40)
        setCurrentStep(1)
        setIsProcessing(false)
        return
      } else {
        throw new Error('Please upload a file or provide a Google Docs URL')
      }

      // Handle file upload
      const response = await fetch(`${config.getApiUrl()}/api/resume/ingest`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('Failed to ingest resume')
      }

      const data = await response.json()
      setResumeData(data)
      setProgress(40)
      setCurrentStep(1)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsProcessing(false)
    }
  }

  const optimizeResume = async () => {
    setIsProcessing(true)
    setError('')
    setProgress(60)

    try {
      const response = await fetch(`${config.getApiUrl()}/api/resume/optimize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resumeStructuredDraft: resumeData.resumeStructuredDraft,
          jd: jobDescription,
          region,
          seniority,
          tone
        })
      })

      if (!response.ok) {
        throw new Error('Failed to optimize resume')
      }

      const data = await response.json()
      setOptimizedData(data)
      setProgress(80)
      setCurrentStep(2)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsProcessing(false)
    }
  }

  const renderLatex = async () => {
    setIsProcessing(true)
    setError('')
    setProgress(90)

    try {
      const response = await fetch(`${config.getApiUrl()}/api/resume/render`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          optimizedJson: optimizedData.optimizedJson
        })
      })

      if (!response.ok) {
        throw new Error('Failed to render LaTeX')
      }

      const data = await response.json()
      setTexString(data.texString)
      setProgress(100)
      setCurrentStep(3)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsProcessing(false)
    }
  }

  const downloadPDF = async () => {
    setIsProcessing(true)
    setError('')

    try {
      const response = await fetch(`${config.getApiUrl()}/api/resume/compile`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          texString
        })
      })

      if (!response.ok) {
        throw new Error('Failed to compile PDF')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'optimized_resume.pdf'
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      setCurrentStep(4)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsProcessing(false)
    }
  }

  const downloadTeX = () => {
    const blob = new Blob([texString], { type: 'text/plain' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'optimized_resume.tex'
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  }

  const renderExperienceDiff = () => {
    if (!resumeData || !optimizedData) return null

    const originalExp = resumeData.resumeStructuredDraft?.experience || []
    const optimizedExp = optimizedData.optimizedJson?.experience || []

    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">Experience Bullets Comparison</h3>
        {originalExp.map((exp, expIndex) => {
          const optimizedExpItem = optimizedExp[expIndex]
          if (!optimizedExpItem) return null

          return (
            <Card key={expIndex} className="p-4">
              <h4 className="font-medium mb-2">{exp.role} at {exp.company}</h4>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <Label className="text-sm font-medium text-red-600">Original</Label>
                  <ul className="mt-1 space-y-1 text-sm">
                    {(exp.bullets || []).map((bullet, bulletIndex) => (
                      <li key={bulletIndex} className="text-gray-600">
                        • {typeof bullet === 'string' ? bullet : bullet.text}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <Label className="text-sm font-medium text-green-600">Optimized</Label>
                  <ul className="mt-1 space-y-1 text-sm">
                    {(optimizedExpItem.bullets || []).map((bullet, bulletIndex) => (
                      <li key={bulletIndex} className="text-gray-600">
                        • {bullet.text}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </Card>
          )
        })}
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">ResumeRefiner</h1>
          <p className="text-lg text-gray-600">AI-Powered Resume Optimization</p>
        </div>

        {/* Progress Bar */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <div className="flex justify-between items-center mb-4">
              {steps.map((step, index) => (
                <div key={index} className="flex items-center">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                    index <= currentStep ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'
                  }`}>
                    {index < currentStep ? <CheckCircle className="w-4 h-4" /> : index + 1}
                  </div>
                  {index < steps.length - 1 && (
                    <div className={`w-16 h-1 mx-2 ${
                      index < currentStep ? 'bg-blue-600' : 'bg-gray-200'
                    }`} />
                  )}
                </div>
              ))}
            </div>
            <Progress value={progress} className="w-full" />
          </CardContent>
        </Card>

        {/* Error Alert */}
        {error && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">{error}</AlertDescription>
          </Alert>
        )}

        {/* Main Content */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Panel - Input */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="w-5 h-5" />
                  Upload Resume
                </CardTitle>
                <CardDescription>
                  Upload your resume or provide a Google Docs link
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Tabs defaultValue="upload" className="w-full">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="upload">File Upload</TabsTrigger>
                    <TabsTrigger value="gdocs">Google Docs</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="upload" className="space-y-4">
                    <div>
                      <Label htmlFor="file-upload">Choose File</Label>
                      <Input
                        id="file-upload"
                        type="file"
                        accept=".pdf,.docx,.doc"
                        onChange={handleFileUpload}
                        className="mt-1"
                      />
                      {file && (
                        <p className="text-sm text-green-600 mt-1">
                          Selected: {file.name}
                        </p>
                      )}
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="gdocs" className="space-y-4">
                    <div>
                      <Label htmlFor="gdocs-url">Google Docs URL</Label>
                      <Input
                        id="gdocs-url"
                        type="url"
                        placeholder="https://docs.google.com/document/d/..."
                        value={googleDocUrl}
                        onChange={(e) => setGoogleDocUrl(e.target.value)}
                        className="mt-1"
                      />
                    </div>
                  </TabsContent>
                </Tabs>

                <Separator />

                <div>
                  <Label htmlFor="job-description">Job Description (Optional)</Label>
                  <Textarea
                    id="job-description"
                    placeholder="Paste the job description here to optimize your resume for this specific role..."
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    rows={4}
                    className="mt-1"
                  />
                </div>

                <div className="grid grid-cols-1 gap-4">
                  <div>
                    <Label>Region</Label>
                    <Select value={region} onValueChange={setRegion}>
                      <SelectTrigger className="mt-1">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="US">United States</SelectItem>
                        <SelectItem value="UK">United Kingdom</SelectItem>
                        <SelectItem value="EU">European Union</SelectItem>
                        <SelectItem value="Other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label>Seniority Level</Label>
                    <Select value={seniority} onValueChange={setSeniority}>
                      <SelectTrigger className="mt-1">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="entry">Entry Level</SelectItem>
                        <SelectItem value="mid">Mid Level</SelectItem>
                        <SelectItem value="senior">Senior Level</SelectItem>
                        <SelectItem value="exec">Executive</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label>Writing Tone</Label>
                    <Select value={tone} onValueChange={setTone}>
                      <SelectTrigger className="mt-1">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="concise">Concise (8-18 words)</SelectItem>
                        <SelectItem value="standard">Standard (12-22 words)</SelectItem>
                        <SelectItem value="detailed">Detailed (18-30 words)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <Button 
                  onClick={ingestResume} 
                  disabled={isProcessing || (!file && !googleDocUrl)}
                  className="w-full"
                >
                  {isProcessing ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    'Start Optimization'
                  )}
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Right Panel - Results */}
          <div className="lg:col-span-2">
            {currentStep >= 1 && resumeData && (
              <Card className="mb-6">
                <CardHeader>
                  <CardTitle>Resume Parsed Successfully</CardTitle>
                  <CardDescription>
                    {resumeData.rawTextStats?.wordCount} words, {resumeData.rawTextStats?.characterCount} characters
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {resumeData.warnings?.length > 0 && (
                    <Alert className="mb-4">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>
                        {resumeData.warnings.join(', ')}
                      </AlertDescription>
                    </Alert>
                  )}
                  <Button onClick={optimizeResume} disabled={isProcessing}>
                    {isProcessing ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Optimizing with AI...
                      </>
                    ) : (
                      'Optimize with AI'
                    )}
                  </Button>
                </CardContent>
              </Card>
            )}

            {currentStep >= 2 && optimizedData && (
              <Card className="mb-6">
                <CardHeader>
                  <CardTitle>AI Optimization Complete</CardTitle>
                  <CardDescription>
                    Resume optimized using STAR, C.A.R., and XYZ methodologies
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="mb-4">
                    <Label className="text-sm font-medium">ATS Keywords Identified:</Label>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {optimizedData.atsKeywords?.slice(0, 10).map((keyword, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {keyword}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  
                  {renderExperienceDiff()}
                  
                  <div className="mt-4">
                    <Button onClick={renderLatex} disabled={isProcessing}>
                      {isProcessing ? (
                        <>
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                          Generating LaTeX...
                        </>
                      ) : (
                        'Generate PDF'
                      )}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {currentStep >= 3 && texString && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="w-5 h-5" />
                    Download Results
                  </CardTitle>
                  <CardDescription>
                    Your optimized resume is ready for download
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex gap-4">
                    <Button onClick={downloadPDF} disabled={isProcessing}>
                      {isProcessing ? (
                        <>
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                          Compiling...
                        </>
                      ) : (
                        <>
                          <Download className="w-4 h-4 mr-2" />
                          Download PDF
                        </>
                      )}
                    </Button>
                    <Button variant="outline" onClick={downloadTeX}>
                      <Download className="w-4 h-4 mr-2" />
                      Download LaTeX
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

