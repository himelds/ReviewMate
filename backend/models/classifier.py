"""
ReviewMate Rhetorical Sentence Classifier

Loads the fine-tuned DistilBERT model from Hugging Face Hub and provides
a simple interface for classifying sentences from research paper abstracts
into five rhetorical roles.

Model: https://huggingface.co/Himel000/reviewmate-classifier-v1

Usage:
    from backend.models.classifier import RhetoricalClassifier
    
    clf = RhetoricalClassifier()
    label = clf.classify("We propose a novel transformer architecture.")
    # label = "METHODS"
    
    labels = clf.classify_batch([
        "Recent advances in NLP have shown promising results.",
        "We aimed to evaluate the impact of attention mechanisms.",
        "Our model achieves 89.3% accuracy on benchmark tasks."
    ])
    # labels = ["BACKGROUND", "OBJECTIVE", "RESULTS"]
"""

from typing import List, Dict, Optional
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


DEFAULT_MODEL_ID = "Himel000/reviewmate-classifier-v1"
DEFAULT_MAX_LENGTH = 64


class RhetoricalClassifier:
    """
    Sentence-level rhetorical role classifier for research paper abstracts.
    
    Classifies each input sentence into one of five rhetorical roles:
    BACKGROUND, OBJECTIVE, METHODS, RESULTS, CONCLUSIONS.
    """
    
    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        device: Optional[str] = None,
        max_length: int = DEFAULT_MAX_LENGTH,
    ):
        """
        Load the classifier model and tokenizer from Hugging Face Hub.
        
        Args:
            model_id: Hugging Face Hub model identifier.
            device: Device to run inference on ("cuda", "cpu", or None for auto).
            max_length: Maximum token length for input sentences.
        """
        self.model_id = model_id
        self.max_length = max_length
        
        # Auto-detect device if not specified
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_id)
        self.model.to(self.device)
        self.model.eval()
        
        # Label mappings from model config
        self.id2label = self.model.config.id2label
        self.label2id = self.model.config.label2id
    
    def classify(self, sentence: str) -> str:
        """
        Classify a single sentence into a rhetorical role.
        
        Args:
            sentence: A sentence from a research abstract.
        
        Returns:
            Predicted label as a string: one of BACKGROUND, OBJECTIVE,
            METHODS, RESULTS, or CONCLUSIONS.
        """
        return self.classify_batch([sentence])[0]
    
    def classify_batch(self, sentences: List[str]) -> List[str]:
        """
        Classify a batch of sentences in a single forward pass.
        
        Args:
            sentences: List of sentences from research abstracts.
        
        Returns:
            List of predicted labels, one per input sentence.
        """
        if not sentences:
            return []
        
        # Tokenize batch
        inputs = self.tokenizer(
            sentences,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        ).to(self.device)
        
        # Forward pass
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Get predicted class IDs
        predicted_ids = outputs.logits.argmax(dim=-1).tolist()
        
        # Convert to label strings
        return [self.id2label[pred_id] for pred_id in predicted_ids]
    
    def classify_with_scores(self, sentence: str) -> Dict[str, float]:
        """
        Classify a sentence and return probability scores for all classes.
        
        Args:
            sentence: A sentence from a research abstract.
        
        Returns:
            Dictionary mapping each label to its predicted probability.
        """
        inputs = self.tokenizer(
            sentence,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        probabilities = torch.softmax(outputs.logits, dim=-1).squeeze().tolist()
        
        return {
            self.id2label[i]: prob
            for i, prob in enumerate(probabilities)
        }
    
    def __repr__(self) -> str:
        return (
            f"RhetoricalClassifier("
            f"model_id='{self.model_id}', "
            f"device='{self.device}', "
            f"max_length={self.max_length})"
        )


if __name__ == "__main__":
    # Quick smoke test when run directly
    print("Loading ReviewMate Rhetorical Classifier...")
    clf = RhetoricalClassifier()
    print(f"Loaded: {clf}\n")
    
    test_sentences = [
        "Recent advances in transformer architectures have demonstrated state-of-the-art performance.",
        "We aimed to investigate whether scaling improves reasoning capabilities.",
        "We trained a 7B parameter model on 1.4 trillion tokens using PyTorch.",
        "Our model achieves 89.3% accuracy, outperforming the previous baseline by 4.2%.",
        "These findings suggest that scaling is a promising direction for future research.",
    ]
    
    print("Classifying test sentences:")
    labels = clf.classify_batch(test_sentences)
    for sent, label in zip(test_sentences, labels):
        print(f"  [{label:12s}] {sent[:70]}...")
