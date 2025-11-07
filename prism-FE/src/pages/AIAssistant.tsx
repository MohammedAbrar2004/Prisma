import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Bot, User } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";

type Message = {
  role: "user" | "assistant";
  content: string;
};

const initialMessages: Message[] = [
  {
    role: "assistant",
    content: "Hello Riya! I'm your AI procurement assistant. I can help you with demand forecasting, procurement optimization, and scenario analysis. What would you like to know?",
  },
  {
    role: "user",
    content: "What if project PWR-002 is delayed by 2 months?",
  },
  {
    role: "assistant",
    content: "If PWR-002 is delayed by 2 months, here's the impact:\n\n• Cement demand will increase by 12% due to extended timeline\n• Steel rods inventory can be redirected to PWR-005\n• Overall budget impact: ₹2.3L additional holding costs\n• Recommendation: Negotiate extended supplier contracts now to lock in current prices",
  },
];

const AIAssistant = () => {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        role: "assistant",
        content: "I'm processing your request. This is a demo response. In production, I would analyze your data and provide specific insights based on your query.",
      };
      setMessages((prev) => [...prev, aiMessage]);
    }, 1000);

    setInput("");
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">AI Assistant</h1>
        <p className="text-muted-foreground mt-2">Ask questions about your supply chain and get instant insights</p>
      </div>

      <Card className="h-[600px] flex flex-col">
        <CardHeader className="border-b border-border">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center">
              <Bot className="h-5 w-5 text-primary-foreground" />
            </div>
            <CardTitle>PRISM AI Assistant</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="flex-1 flex flex-col p-0">
          <ScrollArea className="flex-1 p-6">
            <div className="space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  {message.role === "assistant" && (
                    <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                      <Bot className="h-5 w-5 text-primary-foreground" />
                    </div>
                  )}
                  <div
                    className={`rounded-lg px-4 py-3 max-w-[80%] ${
                      message.role === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted text-foreground"
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  </div>
                  {message.role === "user" && (
                    <div className="h-8 w-8 rounded-full bg-accent flex items-center justify-center flex-shrink-0">
                      <User className="h-5 w-5 text-accent-foreground" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          </ScrollArea>
          <div className="border-t border-border p-4">
            <div className="flex gap-2">
              <Input
                placeholder="Ask about forecasts, inventory, or procurement..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                className="flex-1"
              />
              <Button onClick={handleSend} size="icon">
                <Send className="h-4 w-4" />
              </Button>
            </div>
            <p className="text-xs text-muted-foreground mt-2">
              Try asking: "Show me inventory alerts" or "Compare supplier prices"
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AIAssistant;
