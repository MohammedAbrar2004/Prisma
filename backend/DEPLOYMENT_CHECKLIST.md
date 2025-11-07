# PRISMA Backend Deployment Checklist

Use this checklist when deploying PRISMA to production.

## 🔍 Pre-Deployment

### Code Quality

- [ ] All tests pass
- [ ] No linter errors
- [ ] Type checking passes (`mypy`)
- [ ] Code formatted (`black`)
- [ ] No sensitive data in code
- [ ] All TODO comments resolved

### Dependencies

- [ ] `requirements.txt` is up to date
- [ ] All package versions pinned
- [ ] No security vulnerabilities (`pip-audit`)
- [ ] Unused dependencies removed

### Configuration

- [ ] `.env` file is NOT committed
- [ ] `.env.example` is up to date
- [ ] All required environment variables documented
- [ ] Default values are safe for production

## 🔐 Security

### API Keys

- [ ] API keys stored in secure vault (not `.env`)
- [ ] Keys have minimum required permissions
- [ ] Separate keys for dev/staging/production
- [ ] Key rotation policy in place

### Authentication

- [ ] API authentication implemented
- [ ] Rate limiting configured
- [ ] CORS properly configured (no `*` wildcards)
- [ ] Input validation on all endpoints
- [ ] SQL injection protection (if using DB)

### Network Security

- [ ] HTTPS enabled
- [ ] SSL certificate valid
- [ ] Security headers configured
- [ ] No exposed debug endpoints in production

## 🗄️ Database (if applicable)

- [ ] Migrations tested
- [ ] Backup strategy in place
- [ ] Connection pooling configured
- [ ] Indexes created on frequently queried fields
- [ ] Sensitive data encrypted at rest

## 📊 Monitoring

### Logging

- [ ] Structured logging implemented
- [ ] Log levels appropriate (INFO for production)
- [ ] No sensitive data in logs
- [ ] Log aggregation configured (e.g., ELK stack)

### Metrics

- [ ] Health check endpoint working (`/health`)
- [ ] API metrics collected
- [ ] Error rate monitoring
- [ ] Response time tracking
- [ ] External API status monitoring (`/signals/health/check`)

### Alerts

- [ ] High error rate alerts
- [ ] Service down alerts
- [ ] API quota alerts
- [ ] Performance degradation alerts

## 🚀 Performance

### Caching

- [ ] Response caching implemented (Redis)
- [ ] Cache invalidation strategy
- [ ] Cache hit rate monitoring

### Optimization

- [ ] Database queries optimized
- [ ] Async operations for I/O
- [ ] Connection pooling for external APIs
- [ ] Static assets CDN (if applicable)

### Load Testing

- [ ] Load tests performed
- [ ] Performance benchmarks documented
- [ ] Auto-scaling configured
- [ ] Resource limits set

## 🌐 Infrastructure

### Server

- [ ] Production server provisioned
- [ ] OS security patches applied
- [ ] Firewall configured
- [ ] Non-root user for application
- [ ] Process manager configured (systemd, PM2, etc.)

### Deployment

- [ ] CI/CD pipeline configured
- [ ] Automated testing in pipeline
- [ ] Blue-green or canary deployment
- [ ] Rollback plan documented
- [ ] Deployment runbook created

### Backup & Recovery

- [ ] Automated backups configured
- [ ] Backup restoration tested
- [ ] Disaster recovery plan documented
- [ ] RTO/RPO defined

## 📝 Documentation

### Technical Docs

- [ ] API documentation up to date
- [ ] Architecture diagrams current
- [ ] Deployment guide complete
- [ ] Troubleshooting guide available

### Operational Docs

- [ ] On-call runbook created
- [ ] Incident response procedures
- [ ] Monitoring dashboard setup
- [ ] Contact list for escalations

## 🧪 Testing

### Pre-Production

- [ ] Staging environment matches production
- [ ] All tests pass in staging
- [ ] Smoke tests prepared
- [ ] Regression tests run

### Production Verification

- [ ] Health checks passing
- [ ] All endpoints responding
- [ ] External API connections working
- [ ] Monitoring shows green
- [ ] Sample requests successful

## 📱 Communication

### Team

- [ ] Deployment scheduled
- [ ] Team notified of deployment window
- [ ] On-call engineer assigned
- [ ] Status page updated

### Users

- [ ] Maintenance window announced (if needed)
- [ ] Release notes prepared
- [ ] Support team briefed
- [ ] Documentation updated

## 🔄 Post-Deployment

### Immediate (0-1 hour)

- [ ] Smoke tests run in production
- [ ] Health checks green
- [ ] Error rates normal
- [ ] Response times acceptable
- [ ] External APIs connecting

### Short-term (1-24 hours)

- [ ] Monitor error logs
- [ ] Check API usage patterns
- [ ] Verify data accuracy
- [ ] User feedback collected
- [ ] Performance metrics reviewed

### Medium-term (1-7 days)

- [ ] No critical bugs reported
- [ ] Performance stable
- [ ] Resource usage within limits
- [ ] No security incidents
- [ ] User satisfaction acceptable

## 🐛 Rollback Plan

### Triggers

- [ ] Error rate > X%
- [ ] Response time > Y seconds
- [ ] Critical bug discovered
- [ ] Security vulnerability found

### Procedure

1. [ ] Stop new deployments
2. [ ] Revert to previous version
3. [ ] Verify rollback successful
4. [ ] Notify stakeholders
5. [ ] Document incident
6. [ ] Plan fix

## 📋 Environment-Specific Checklists

### Development

- [ ] Local `.env` configured
- [ ] Test data available
- [ ] Debug mode enabled
- [ ] Hot-reload working

### Staging

- [ ] Production-like data
- [ ] All integrations working
- [ ] Performance testing enabled
- [ ] Staging API keys configured

### Production

- [ ] Production API keys
- [ ] Debug mode disabled
- [ ] HTTPS enforced
- [ ] Monitoring active
- [ ] Backups running

## 🎯 PRISMA-Specific Checks

### External APIs

- [ ] MetalpriceAPI key configured and tested
- [ ] CommodityAPI key configured and tested
- [ ] WeatherAPI key configured and tested
- [ ] World Bank API accessible
- [ ] API rate limits documented
- [ ] Fallback to mock data working

### Signals Engine

- [ ] `/signals/{company_id}` working
- [ ] Region filtering working
- [ ] Material filtering working
- [ ] Signal generation under X seconds
- [ ] Mock data mode working
- [ ] Data sources correctly attributed

### Data Quality

- [ ] Signal scores in 0.0-1.0 range
- [ ] Confidence values reasonable
- [ ] Drivers are human-readable
- [ ] Timestamps in ISO format
- [ ] No null/undefined in critical fields

## 🔍 Final Verification

Before marking deployment complete:

```bash
# Test health
curl https://your-domain.com/health

# Test signals
curl https://your-domain.com/signals/test-company

# Test API health
curl https://your-domain.com/signals/health/check

# Check logs for errors
# Check monitoring dashboard
# Verify metrics are flowing
```

## 📝 Sign-off

- [ ] Technical lead approval
- [ ] Security review passed
- [ ] Performance requirements met
- [ ] Documentation complete
- [ ] Team trained on new features

**Deployment Date:** _______________

**Deployed By:** _______________

**Approved By:** _______________

**Version:** _______________

---

## 🆘 Emergency Contacts

**On-Call Engineer:** _______________

**Infrastructure Team:** _______________

**Security Team:** _______________

**Stakeholders:** _______________

---

## 📚 Related Documents

- [SETUP.md](SETUP.md) - Setup instructions
- [README.md](README.md) - Main documentation
- [API_GUIDE.md](API_GUIDE.md) - API usage
- [PROJECT_SUMMARY.md](../PROJECT_SUMMARY.md) - Implementation summary

---

**Remember:** It's better to delay deployment than to rush and cause an incident. When in doubt, run more tests! 🛡️

