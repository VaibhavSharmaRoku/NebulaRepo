package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
)

func main() {
	cfg, _ := config.LoadDefaultConfig(context.TODO(), config.WithRegion("us-east-1"))
	result, err := s3.NewFromConfig(cfg).ListBuckets(context.TODO(), &s3.ListBucketsInput{})
	if err != nil {
		log.Fatalf("Error: %v", err)
	}

	fmt.Println("\nBucket Name                            Creation Date")
	fmt.Println("--------------------------------------------------")
	for _, b := range result.Buckets {
		fmt.Printf("%-40s %s\n", aws.ToString(b.Name), b.CreationDate.Format(time.RFC1123))
	}
	fmt.Printf("\nTotal buckets: %d\n", len(result.Buckets))
}
